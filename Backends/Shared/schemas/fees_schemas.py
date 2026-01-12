# Backends/Backend_admin/schemas/fees_schemas.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus
from Backends.Shared.enums.fee_payments_enums import FeePaymentStatus
from Backends.Shared.enums.fees_enums import BillingType, FeeFrequency, ChargeTrigger, FeeGeneratedBy
from Backends.Shared.enums.fee_payments_enums import (
    PaymentSource, PaymentReceivedBy
)
from Backends.Shared.enums.fee_audit_enums import (
    FeeAuditEntity, FeeAuditAction, AuditActorRole, AuditSource
)


# ----Fee Master (for class-level fees)----
class FeeMasterCreate(BaseModel):
    class_id: int
    fee_type: str

    billing_type: BillingType
    frequency: FeeFrequency | None = None
    charge_trigger: ChargeTrigger = ChargeTrigger.ACADEMIC_CYCLE

    amount: Decimal
    currency: str = "INR"

    allow_proration: bool = False
    is_mandatory: bool = True

    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    notes: Optional[str] = None
    display_order: int = 1

    class Config:
        from_attributes = True


class FeeMasterResponse(FeeMasterCreate):
    fee_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class FeeMasterUpdate(BaseModel):
    fee_type: Optional[str]
    amount: Optional[Decimal]
    effective_from: Optional[date]
    effective_to: Optional[date]
    notes: Optional[str]

    class Config:
        from_attributes = True
        


# ----Student Fee (invoice / due details)----
class StudentFeeCreate(BaseModel):
    student_id: int
    class_id: int
    fee_id: Optional[int]
    amount_due: Decimal = Field(..., gt=0)
    due_date: date
    class Config:
        from_attributes = True



class StudentFeeOut(BaseModel):
    invoice_id: int
    student_id: int
    class_id: int
    fee_id: Optional[int]

    amount_due: Decimal
    amount_paid: Decimal

    due_date: date
    status: StudentFeeStatus

    billing_type: BillingType
    frequency: FeeFrequency | None
    charge_trigger: ChargeTrigger

    billing_period_start: Optional[date]
    billing_period_end: Optional[date]

    generated_by: FeeGeneratedBy
    is_active: bool

    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True



# ----Fee payments (actual transactions)----
class FeePaymentCreate(BaseModel):
    invoice_id: int
    student_id: int
    amount: Decimal

    payment_method_id: int
    payer_id: Optional[int] = None

    payment_source: PaymentSource
    billing_cycle: Optional[date] = None
    is_partial_payment: bool = False
    received_by: PaymentReceivedBy = PaymentReceivedBy.ONLINE
    remarks: Optional[str] = None

    class Config:
        from_attributes = True



class FeePaymentResponse(BaseModel):
    payment_id: int
    invoice_id: int
    student_id: int

    amount: Decimal
    payment_method_id: int
    payment_method_name: str

    status: FeePaymentStatus
    payment_source: PaymentSource
    received_by: PaymentReceivedBy
    is_partial_payment: bool

    created_at: datetime

    class Config:
        from_attributes = True




# ----payment method schemas----
class PaymentMethodBase(BaseModel):
    method_name: str = Field(..., min_length=2, max_length=50)
    class Config:
        from_attributes = True

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    method_name: str | None = Field(None, min_length=2, max_length=50)
    is_active: bool | None = None
    class Config:
        from_attributes = True

class PaymentMethodResponse(BaseModel):
    method_id: int
    method_name: str
    is_active: bool
    class Config:
        from_attributes = True

# --receipt upload response--
class UploadReceiptResponse(BaseModel):
    message: str
    invoice_id: int
    receipt_path: str | None = None
    receipt_url: str | None = None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now())

    class Config:
        from_attributes = True




# ---- Fee Audit Schemas ----
class FeeAuditResponse(BaseModel):
    audit_id: int
    invoice_id: int
    changed_by: int

    entity_type: FeeAuditEntity
    action: FeeAuditAction
    changed_by_role: AuditActorRole
    reason: Optional[str]
    source: AuditSource

    before_change: dict | None
    after_change: dict | None
    ts: datetime

    class Config:
        from_attributes = True


class FeeAuditListResponse(BaseModel):
    items: list[FeeAuditResponse]
    total: int
    class Config:
        from_attributes = True


class FeePayCreate(BaseModel):
    invoice_id: int
    amount: Decimal
    payment_method_id: int
    payment_source: PaymentSource = PaymentSource.ADMIN
    class Config:
        from_attributes = True


class FeeRefundCreate(BaseModel):
    payment_id: int
    reason: Optional[str] = None
    class Config:
        from_attributes = True
