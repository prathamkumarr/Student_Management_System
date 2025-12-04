# Backends/Backend_admin/schemas/fees_schemas.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Annotated
from decimal import Decimal

# ----Fee Master (for class-level fees)----
class FeeMasterCreate(BaseModel):
    class_id: int
    fee_type: str
    amount: Decimal = Field(..., ge=0, le=9999999999, description="Fee amount (up to 10 digits, 2 decimals)")
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True

class FeeMasterResponse(FeeMasterCreate):
    fee_id: int
    is_active: bool
    currency: str = "INR"
    created_at: datetime
    class Config:
        from_attributes = True

# ----Student Fee (invoice / due details)----
class StudentFeeCreate(BaseModel):
    student_id: int
    class_id: int
    fee_id: Optional[int]
    amount_due: Decimal = Field(..., gt=0, le=9999999999, description="Fee amount (up to 10 digits, 2 decimals)")
    due_date: date
    class Config:
        from_attributes = True

class StudentFeeOut(BaseModel):
    invoice_id: int
    student_id: int
    class_id: int
    fee_id: Optional[int] = None
    amount_due: float
    amount_paid: float
    due_date: date
    status: str
    class Config:
        from_attributes = True



# ----Fee payments (actual transactions)----
class FeePaymentCreate(BaseModel):
    invoice_id: int
    student_id: int
    amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    payment_method: str
    payment_provider: Optional[str] = None
    payer_id: Optional[int] = None
    payment_method_id: int = Field(..., gt=0)
    class Config:
        from_attributes = True

class FeePaymentResponse(BaseModel):
    payment_id: int
    invoice_id: int
    student_id: int
    amount: Decimal
    method_id: int
    payment_method: str       
    payment_method_name: str      
    status: str
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

# ---razorpay---
class RazorpayOrderCreate(BaseModel):
    invoice_id: int
    student_id: int
    amount: Decimal
    class Config:
        from_attributes = True

class RazorpayVerify(BaseModel):
    invoice_id: int
    student_id: int
    amount: Decimal
    method_id: int

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    class Config:
        from_attributes = True

