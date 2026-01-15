# fees_router.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from Backends.Shared.models.fees_models import StudentFee, FeePayment
from Backends.Shared.models.payment_method import PaymentMethod
from Backends.Shared.schemas.fees_schemas import (
    PaymentMethodResponse,
    FeePaymentCreate, 
    FeePaymentResponse,
)
from fastapi.responses import FileResponse
from fpdf import FPDF  
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus
from Backends.Shared.enums.fee_payments_enums import FeePaymentStatus
from Backends.Shared.enums.fee_payments_enums import(
    PaymentSource, PaymentReceivedBy
)

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
    
    if invoice.status == StudentFeeStatus.PAID:
        raise HTTPException(400, "Invoice already fully paid")

    # Payment method check
    method = db.query(PaymentMethod).filter(
        PaymentMethod.method_id == data.payment_method_id,
        PaymentMethod.is_active == True
    ).first()

    if not method:
        raise HTTPException(400, "Invalid payment method")
    
    if invoice.amount_paid + data.amount > invoice.amount_due:
        raise HTTPException(
            status_code=400,
            detail="Overpayment not allowed"
        )

    # Create payment
    payment = FeePayment(
    invoice_id=data.invoice_id,
    student_id=data.student_id,
    amount=data.amount,
    payment_method_id=data.payment_method_id,
    payment_method_name=method.method_name,
    payment_source=PaymentSource.STUDENT,
    received_by=PaymentReceivedBy.ONLINE,
    academic_session_id=invoice.academic_session_id,
    is_partial_payment=invoice.amount_paid + data.amount < invoice.amount_due
    )

    invoice.amount_paid += data.amount

    # Auto update invoice status
    if invoice.amount_paid >= invoice.amount_due:
        invoice.status = StudentFeeStatus.PAID
    elif invoice.amount_paid > 0:
        invoice.status = StudentFeeStatus.PARTIALLY_PAID
    else:
        invoice.status = StudentFeeStatus.PENDING

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
        payment_source=payment.payment_source,
        received_by=payment.received_by,
        is_partial_payment=payment.is_partial_payment,
        created_at=payment.created_at
    )

# endpoint to store & track that payment
@router.get("/history/{student_id}", response_model=list[FeePaymentResponse])
def history(student_id: int, db: Session = Depends(get_db)):

    payments = (
        db.query(FeePayment)
        .filter(
            FeePayment.student_id == student_id,
            FeePayment.status == FeePaymentStatus.SUCCESS
        )
        .order_by(FeePayment.created_at.desc())
        .all()
    )

    return [
        FeePaymentResponse(
            payment_id=p.payment_id,
            invoice_id=p.invoice_id,
            student_id=p.student_id,
            amount=p.amount,

            payment_method_id=p.payment_method_id,
            payment_method_name=p.payment_method_name,

            status=p.status,
            payment_source=p.payment_source,
            received_by=p.received_by,
            is_partial_payment=p.is_partial_payment,

            created_at=p.created_at
        )
        for p in payments
    ]

# endpoint for viewing history and downloading receipts
@router.get("/receipt/{invoice_id}")
def download_receipt(invoice_id: int, db: Session = Depends(get_db)):

    # ---- Invoice ----
    invoice = (
        db.query(StudentFee)
        .filter(
            StudentFee.invoice_id == invoice_id,
            StudentFee.is_active == True
        )
        .first()
    )

    if not invoice:
        raise HTTPException(404, "Invoice not found")

    # ---- Payments ----
    payments = (
        db.query(FeePayment)
        .filter(
            FeePayment.invoice_id == invoice_id,
            FeePayment.status == FeePaymentStatus.SUCCESS
        )
        .order_by(FeePayment.created_at.asc())
        .all()
    )

    if not payments:
        raise HTTPException(400, "No successful payment found for this invoice")

    # ---- PDF ----
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    pdf.add_font("ArialUnicode", "", font_path, uni=True)
    pdf.set_font("ArialUnicode", size=12)

    # ---- Header ----
    pdf.cell(0, 10, "SCHOOL FEE RECEIPT", ln=True, align="C")
    pdf.ln(5)

    # ---- Invoice Info ----
    pdf.cell(0, 8, f"Invoice ID: {invoice.invoice_id}", ln=True)
    pdf.cell(0, 8, f"Student ID: {invoice.student_id}", ln=True)
    pdf.cell(0, 8, f"Class ID: {invoice.class_id}", ln=True)
    pdf.cell(0, 8, f"Total Amount: ₹{invoice.amount_due}", ln=True)
    pdf.cell(0, 8, f"Amount Paid: ₹{invoice.amount_paid}", ln=True)
    pdf.cell(0, 8, f"Status: {invoice.status.value}", ln=True)
    pdf.cell(0, 8, f"Due Date: {invoice.due_date}", ln=True)

    # ---- Payments ----
    pdf.ln(10)
    pdf.cell(0, 8, "Payment Records:", ln=True)
    pdf.ln(3)

    for p in payments:
        pdf.multi_cell(
            0,
            8,
            (
                f"Method: {p.payment_method_name} | "
                f"Amount: ₹{p.amount} | "
                f"Date: {p.created_at.strftime('%Y-%m-%d')}"
            )
        )

    # ---- Stream ----
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=receipt_{invoice.invoice_id}.pdf"
        },
    )

# endpoint to view pending fees by student ID
@router.get("/pending/{student_id}")
def get_pending_fee(student_id: int, db: Session = Depends(get_db)):

    invoices = db.query(StudentFee).filter(
        StudentFee.student_id == student_id,
        StudentFee.is_active == True,
        StudentFee.status.in_([
            StudentFeeStatus.PENDING,
            StudentFeeStatus.PARTIALLY_PAID
        ])
    ).all()

    if not invoices:
        raise HTTPException(404, "No pending fee records found")

    return [
        {
            "invoice_id": i.invoice_id,
            "class_id": i.class_id,
            "amount_due": i.amount_due,
            "amount_paid": i.amount_paid,
            "pending_amount": i.amount_due - i.amount_paid,
            "status": i.status.value,
            "due_date": i.due_date
        }
        for i in invoices
    ]

