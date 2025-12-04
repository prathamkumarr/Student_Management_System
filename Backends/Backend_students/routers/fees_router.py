# fees_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from Backends.Shared.models.fees_models import StudentFee, FeePayment
from Backends.Shared.models.payment_method import PaymentMethod
from Backends.Shared.schemas.fees_schemas import (
    PaymentMethodResponse, RazorpayOrderCreate, RazorpayVerify,
    FeePaymentCreate, 
    FeePaymentResponse,
)
from Backends.Shared.razorpay_client import razorpay_client
from fastapi.responses import FileResponse
from fpdf import FPDF  # lightweight lib for generating PDFs
import os

router = APIRouter(prefix="/fees", tags=["Fees Management"])

# ednpoint to view all payment methods
@router.get("/payment-methods", response_model=list[PaymentMethodResponse])
def get_methods(db: Session = Depends(get_db)):
    return db.query(PaymentMethod).filter(PaymentMethod.is_active == True).all()

# endpoint for making the payment (by student/parent)
@router.post("/pay", response_model=FeePaymentResponse)
def pay_fee(data: FeePaymentCreate, db: Session = Depends(get_db)):

    # Invoice check
    invoice = db.query(StudentFee).filter(
        StudentFee.invoice_id == data.invoice_id
    ).first()

    if not invoice:
        raise HTTPException(404, "Invoice not found")

    # Payment method check
    method = db.query(PaymentMethod).filter(
        PaymentMethod.method_id == data.payment_method_id,
        PaymentMethod.is_active == True
    ).first()

    if not method:
        raise HTTPException(400, "Invalid payment method")

    # Create payment
    payment = FeePayment(
        invoice_id=data.invoice_id,
        student_id=data.student_id,
        amount=data.amount,
        payment_method_id=data.payment_method_id
    )

    invoice.amount_paid += data.amount

    # Auto update invoice status
    if invoice.amount_paid >= invoice.amount_due:
        invoice.status = "paid"
    elif invoice.amount_paid > 0:
        invoice.status = "partially_paid"
    else:
        invoice.status = "pending"

    db.add(payment)
    db.commit()

    # Join method name for response
    return FeePaymentResponse(
        payment_id=payment.payment_id,
        invoice_id=payment.invoice_id,
        student_id=payment.student_id,
        amount=payment.amount,
        payment_method_id=method.method_id,
        payment_method_name=method.method_name,
        status=payment.status,
        created_at=payment.created_at
    )

# endpoint to create order using razorpay
@router.post("/create-order")
def create_order(payload: RazorpayOrderCreate, db: Session = Depends(get_db)):

    invoice = db.query(StudentFee).filter(StudentFee.invoice_id == payload.invoice_id).first()
    if not invoice:
        raise HTTPException(404, "Invoice not found")

    # Convert amount to paise → ₹100 = 10000
    amount_paise = int(float(payload.amount) * 100)

    order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": f"inv_{invoice.invoice_id}",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": payload.amount,
        "currency": "INR",
        "invoice_id": invoice.invoice_id,
        "key_id": os.getenv("RAZORPAY_KEY_ID")
    }

# endpoint for verification
@router.post("/verify")
def verify_payment(data: RazorpayVerify, db: Session = Depends(get_db)):

    params_dict = {
        "razorpay_order_id": data.razorpay_order_id,
        "razorpay_payment_id": data.razorpay_payment_id,
        "razorpay_signature": data.razorpay_signature
    }

    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
    except:
        raise HTTPException(400, "Payment signature verification failed")

    # Store payment record
    payment = FeePayment(
        invoice_id=data.invoice_id,
        student_id=data.student_id,
        amount=data.amount,
        payment_method_id=data.method_id,  # Razorpay method
        status="success"
    )
    db.add(payment)

    # Update invoice
    invoice = db.query(StudentFee).get(data.invoice_id)
    invoice.amount_paid += data.amount

    if invoice.amount_paid >= invoice.amount_due:
        invoice.status = "paid"
    else:
        invoice.status = "partially_paid"

    db.commit()
    return {"message": "Payment verified & recorded successfully"}

# endpoint to store & track that payment
@router.get("/history/{student_id}", response_model=list[FeePaymentResponse])
def history(student_id: int, db: Session = Depends(get_db)):

    payments = (
        db.query(FeePayment)
        .filter(FeePayment.student_id == student_id)
        .order_by(FeePayment.created_at.desc())
        .all()
    )

    return [
    FeePaymentResponse(
        payment_id=p.payment_id,
        invoice_id=p.invoice_id,
        student_id=p.student_id,
        amount=p.amount,
        method_id=p.payment_method_id if p.payment_method_id is not None else 0,
        payment_method=(
            p.payment_method_rel.method_name 
            if p.payment_method_rel else "Unknown"
        ),

        payment_method_name=(
            p.payment_method_rel.method_name 
            if p.payment_method_rel else "Unknown"
        ),

        status=p.status,
        created_at=p.created_at
    )
    for p in payments
]

# endpoint for viewing history and downloading receipts
@router.get("/receipt/{invoice_id}")
def download_receipt(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(StudentFee).filter(StudentFee.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    payments = db.query(FeePayment).filter(FeePayment.invoice_id == invoice_id).all()

    pdf = FPDF()
    pdf.add_page()

    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    pdf.add_font("ArialUnicode", "", font_path, uni=True)
    pdf.set_font("ArialUnicode", size=12)

    pdf.cell(200, 10, txt="SCHOOL FEE RECEIPT", ln=True, align="C")
    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Invoice ID: {invoice.invoice_id}", ln=True)
    pdf.cell(200, 10, txt=f"Student ID: {invoice.student_id}", ln=True)
    pdf.cell(200, 10, txt=f"Class ID: {invoice.class_id}", ln=True)
    pdf.cell(200, 10, txt=f"Total Amount: ₹{invoice.amount_due}", ln=True)
    pdf.cell(200, 10, txt=f"Amount Paid: ₹{invoice.amount_paid}", ln=True)
    pdf.cell(200, 10, txt=f"Status: {invoice.status}", ln=True)
    pdf.cell(200, 10, txt=f"Due Date: {invoice.due_date}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Payment Records:", ln=True)

    for p in payments:
        pdf.cell(
        200, 10,
        txt=f"{p.payment_method_name} | ₹{p.amount} | {p.status} | {p.created_at.strftime('%Y-%m-%d')}",
        ln=True
    )
        
    file_path = f"/tmp/receipt_{invoice.invoice_id}.pdf"
    pdf.output(file_path)
    return FileResponse(file_path, media_type='application/pdf', filename=f"receipt_{invoice.invoice_id}.pdf")

# endpoint to view pending fees by student ID
@router.get("/pending/{student_id}")
def get_pending_fee(student_id: int, db: Session = Depends(get_db)):
    invoices = db.query(StudentFee).filter(StudentFee.student_id == student_id).all()

    if not invoices:
        raise HTTPException(404, "No fee records found")

    pending = [
        {
            "invoice_id": i.invoice_id,
            "class_id": i.class_id,
            "amount_due": i.amount_due,
            "amount_paid": i.amount_paid,
            "status": i.status,
            "due_date": i.due_date
        }
        for i in invoices if i.status != "paid"
    ]

    return pending
