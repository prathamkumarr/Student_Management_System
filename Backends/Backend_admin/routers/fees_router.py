# Backends/Backend_admin/routers/fees_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from Backends.Shared.models.students_master import StudentMaster

from Backends.Shared.connection import get_db
from Backends.Shared.models.fees_models import StudentFee
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Shared.schemas.fees_schemas import (
    FeeMasterCreate, FeeMasterResponse, FeeMasterUpdate,
    StudentFeeCreate, StudentFeeOut
)
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus
from Backends.Shared.enums.fees_enums import (
    BillingType,
    FeeFrequency,
    ChargeTrigger,
    FeeGeneratedBy
)
from Backends.Shared.enums.fee_audit_enums import (
    FeeAuditEntity, FeeAuditAction, AuditActorRole, AuditSource
)
from Backends.Shared.models.fees_models import FeePayment, StudentFee, FeeAudit
from Backends.Shared.enums.fee_payments_enums import FeePaymentStatus, PaymentSource, PaymentReceivedBy
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus

router = APIRouter(prefix="/admin/fees", tags=["Admin Fees Management"])


# ========================================================================
# Fee Master (class-level rules)

# endpoint to create fee of a student 
@router.post("/create", response_model=FeeMasterResponse, status_code=status.HTTP_201_CREATED)
def create_fee(payload: FeeMasterCreate, db: Session = Depends(get_db)):

    normalized_fee_type = payload.fee_type.strip().upper()

    existing = db.query(FeeMaster).filter(
        FeeMaster.class_id == payload.class_id,
        FeeMaster.fee_type == normalized_fee_type,
        FeeMaster.is_active == True
    ).first()

    if existing:
        raise HTTPException(400, "Fee type already exists for this class")

    new_fee = FeeMaster(
        class_id=payload.class_id,
        fee_type=normalized_fee_type,

        billing_type=payload.billing_type,
        frequency=payload.frequency,
        charge_trigger=payload.charge_trigger,

        amount=payload.amount,
        currency=payload.currency or "INR",

        allow_proration=payload.allow_proration,
        is_mandatory=payload.is_mandatory,

        effective_from=payload.effective_from,
        effective_to=payload.effective_to,

        notes=payload.notes,
        display_order=payload.display_order or 1,

        is_active=True
    )

    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)
    return new_fee


# endpoint to view all fees
@router.get("/all", response_model=List[FeeMasterResponse])
def get_all_fee_masters(
    class_id: Optional[int] = None,
    billing_type: Optional[BillingType] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    q = db.query(FeeMaster).filter(FeeMaster.is_active == is_active)

    if class_id:
        q = q.filter(FeeMaster.class_id == class_id)

    if billing_type:
        q = q.filter(FeeMaster.billing_type == billing_type)

    return q.order_by(
        FeeMaster.display_order.asc(),
        FeeMaster.created_at.asc()
    ).all()


# Endpoint to fetch fee details using fee_id
@router.get("/get/{fee_id}", response_model=FeeMasterResponse)
def get_fee_by_id(fee_id: int, db: Session = Depends(get_db)):
    fee = db.query(FeeMaster).filter(
        FeeMaster.fee_id == fee_id,
        FeeMaster.is_active == True
    ).first()

    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    return fee


# endpoint to update fees using fee_id
@router.put("/update/{fee_id}", response_model=FeeMasterResponse)
def update_fee(fee_id: int, payload: FeeMasterUpdate, db: Session = Depends(get_db)):
    fee = db.query(FeeMaster).filter(FeeMaster.fee_id == fee_id).first()

    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    if not fee.is_active:
        raise HTTPException(status_code=400, detail="Inactive fee cannot be updated")

    assigned = db.query(StudentFee).filter(
        StudentFee.fee_id == fee_id,
        StudentFee.is_active == True
    ).first()

    if assigned:
        raise HTTPException(
            status_code=400,
            detail="Fee already assigned to students; cannot be modified"
        )

    updates = payload.model_dump(exclude_unset=True)

    forbidden = {
        "class_id",
        "is_active",
        "created_at",
        "updated_at"
    }

    if forbidden.intersection(updates.keys()):
        raise HTTPException(
            status_code=400,
            detail="One or more fields cannot be updated"
        )

    for k, v in updates.items():
        setattr(fee, k, v)

    db.commit()
    db.refresh(fee)
    return fee


# endpoint to delete any fee using fee_id
@router.delete("/delete/{fee_id}", response_model=FeeMasterResponse)
def delete_fee(fee_id: int, db: Session = Depends(get_db)):
    fee = db.query(FeeMaster).filter(FeeMaster.fee_id == fee_id).first()

    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    if not fee.is_active:
        raise HTTPException(status_code=400, detail="Fee already inactive")

    if fee.is_mandatory:
        raise HTTPException(
            status_code=400,
            detail="Mandatory fee cannot be deleted"
        )

    assigned = db.query(StudentFee).filter(
        StudentFee.fee_id == fee_id,
        StudentFee.is_active == True
    ).first()

    if assigned:
        raise HTTPException(
            status_code=400,
            detail="Fee already assigned to students; cannot be deleted"
        )

    fee.is_active = False
    db.commit()
    db.refresh(fee)

    return fee


# ==================================================================
# Student Fees (invoices)

# endpoint to assign fees to a student 
@router.post("/assign", response_model=StudentFeeOut, status_code=status.HTTP_201_CREATED)
def assign_fee(payload: StudentFeeCreate, db: Session = Depends(get_db)):

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == payload.student_id
    ).first()

    if not student:
        raise HTTPException(404, f"Student ID {payload.student_id} not found")

    if student.is_active is False:
        raise HTTPException(400, "Cannot assign fee — Student has TC")

    fee = None
    if payload.fee_id:
        fee = db.query(FeeMaster).filter(
            FeeMaster.fee_id == payload.fee_id,
            FeeMaster.is_active == True
        ).first()

        if not fee:
            raise HTTPException(400, "Invalid or inactive fee")

        if fee.class_id != payload.class_id:
            raise HTTPException(400, "Fee does not belong to given class")

    existing = db.query(StudentFee).filter(
        StudentFee.student_id == payload.student_id,
        StudentFee.class_id == payload.class_id,
        StudentFee.fee_id == payload.fee_id,
        StudentFee.due_date == payload.due_date,
        StudentFee.is_active == True,
        StudentFee.status != StudentFeeStatus.PAID
    ).first()

    if existing:
        raise HTTPException(400, "Fee already assigned and pending")

    new_invoice = StudentFee(
        student_id=payload.student_id,
        class_id=payload.class_id,
        fee_id=payload.fee_id,

        amount_due=payload.amount_due,
        due_date=payload.due_date,

        billing_type=fee.billing_type,
        frequency=fee.frequency,
        charge_trigger=fee.charge_trigger,
        generated_by=FeeGeneratedBy.ADMIN
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


# endpoint to view all fee history
@router.get("/all/history", response_model=List[StudentFeeOut])
def get_all_student_fees(
    student_id: Optional[int] = None,
    status: Optional[StudentFeeStatus] = None,
    db: Session = Depends(get_db)
):
    q = db.query(StudentFee).filter(StudentFee.is_active == True)

    if student_id:
        q = q.filter(StudentFee.student_id == student_id)

    if status:
        q = q.filter(StudentFee.status == status)

    return q.order_by(StudentFee.created_at.desc()).all()


# =========================================================================
# Fee Payments

@router.post("/pay", status_code=201)
def pay_fee(
    invoice_id: int,
    amount: Decimal,
    payment_method_id: int,
    payment_source: PaymentSource,
    db: Session = Depends(get_db)
):
    invoice = db.query(StudentFee).filter(
        StudentFee.invoice_id == invoice_id,
        StudentFee.is_active == True
    ).first()

    if not invoice:
        raise HTTPException(404, "Invoice not found")

    if invoice.status == StudentFeeStatus.PAID:
        raise HTTPException(400, "Invoice already paid")

    payment = FeePayment(
        invoice_id=invoice.invoice_id,
        student_id=invoice.student_id,
        amount=amount,
        payment_method_id=payment_method_id,
        payment_method_name="AUTO",
        payment_source=payment_source,
        status=FeePaymentStatus.SUCCESS,
        received_by=PaymentReceivedBy.ONLINE
    )

    invoice.amount_paid += amount

    if invoice.amount_paid >= invoice.amount_due:
        invoice.status = StudentFeeStatus.PAID
    else:
        invoice.status = StudentFeeStatus.PARTIALLY_PAID

    audit = FeeAudit(
        invoice_id=invoice.invoice_id,
        changed_by=0,  # admin/system id later
        entity_type=FeeAuditEntity.PAYMENT,
        action=FeeAuditAction.PAYMENT_ADDED,
        changed_by_role=AuditActorRole.ADMIN,
        source=AuditSource.UI,
        after_change={
            "amount_paid": str(invoice.amount_paid),
            "status": invoice.status.value
        }
    )

    db.add_all([payment, audit])
    db.commit()

    return {"message": "Payment successful", "invoice_id": invoice_id}

# ----------------------------------
@router.get("/payments/{invoice_id}")
def get_payments(invoice_id: int, db: Session = Depends(get_db)):
    payments = db.query(FeePayment).filter(
        FeePayment.invoice_id == invoice_id
    ).order_by(FeePayment.created_at.desc()).all()

    return payments


# -----------------------------------
@router.post("/refund")
def refund_payment(
    payment_id: int,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    payment = db.query(FeePayment).filter(
        FeePayment.payment_id == payment_id
    ).first()

    if not payment:
        raise HTTPException(404, "Payment not found")

    if payment.status != FeePaymentStatus.SUCCESS:
        raise HTTPException(400, "Only successful payments can be refunded")

    payment.status = FeePaymentStatus.REFUNDED

    audit = FeeAudit(
        invoice_id=payment.invoice_id,
        changed_by=0,
        entity_type=FeeAuditEntity.PAYMENT,
        action=FeeAuditAction.PAYMENT_REVERSED,
        changed_by_role=AuditActorRole.ADMIN,
        reason=reason,
        source=AuditSource.UI
    )

    db.add(audit)
    db.commit()

    return {"message": "Payment refunded"}


# ======================================================================
# Fee Audit

# ------------------------------
@router.get("/audit/{invoice_id}")
def get_fee_audit(invoice_id: int, db: Session = Depends(get_db)):
    audits = db.query(FeeAudit).filter(
        FeeAudit.invoice_id == invoice_id
    ).order_by(FeeAudit.ts.desc()).all()

    return {
        "invoice_id": invoice_id,
        "total": len(audits),
        "items": audits
    }

# ======================================================================
# Fee Generation

# -----------------------------
@router.post("/generate/monthly")
def generate_monthly_fees(
    class_id: int,
    due_date: date,
    db: Session = Depends(get_db)
):
    fees = db.query(FeeMaster).filter(
        FeeMaster.class_id == class_id,
        FeeMaster.billing_type == BillingType.RECURRING,
        FeeMaster.frequency == FeeFrequency.MONTHLY,
        FeeMaster.is_active == True
    ).all()

    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == class_id,
        StudentMaster.is_active == True
    ).all()

    created = 0

    for fee in fees:
        for student in students:
            exists = db.query(StudentFee).filter(
                StudentFee.student_id == student.student_id,
                StudentFee.fee_id == fee.fee_id,
                StudentFee.due_date == due_date
            ).first()

            if exists:
                continue

            invoice = StudentFee(
                student_id=student.student_id,
                class_id=class_id,
                fee_id=fee.fee_id,
                amount_due=fee.amount,
                due_date=due_date,
                billing_type=fee.billing_type,
                frequency=fee.frequency,
                charge_trigger=fee.charge_trigger
            )

            db.add(invoice)
            created += 1

    db.commit()
    return {"generated_invoices": created}


# -------------------------------------
@router.post("/generate/academic")
def generate_academic_fees(
    class_id: int,
    due_date: date,
    db: Session = Depends(get_db)
):
    fees = db.query(FeeMaster).filter(
        FeeMaster.class_id == class_id,
        FeeMaster.charge_trigger == ChargeTrigger.ACADEMIC_CYCLE,
        FeeMaster.is_active == True
    ).all()

    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == class_id,
        StudentMaster.is_active == True
    ).all()

    created = 0

    for fee in fees:
        for student in students:
            exists = db.query(StudentFee).filter(
                StudentFee.student_id == student.student_id,
                StudentFee.fee_id == fee.fee_id
            ).first()

            if exists:
                continue

            invoice = StudentFee(
                student_id=student.student_id,
                class_id=class_id,
                fee_id=fee.fee_id,
                amount_due=fee.amount,
                due_date=due_date,
                billing_type=fee.billing_type,
                charge_trigger=fee.charge_trigger
            )

            db.add(invoice)
            created += 1

    db.commit()
    return {"generated_invoices": created}


# get active fees for a class
@router.get("/class/{class_id}", response_model=list[FeeMasterResponse])
def get_fees_by_class(class_id: int, db: Session = Depends(get_db)):

    fees = db.query(FeeMaster).filter(
        FeeMaster.class_id == class_id,
        FeeMaster.is_active == True
    ).order_by(FeeMaster.display_order).all()

    return fees



@router.get("/student/{student_id}/class")
def get_student_active_class(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found or inactive")

    if not student.class_id:
        raise HTTPException(400, "Student is not assigned to any class")

    return {
        "class_id": student.class_id
    }
