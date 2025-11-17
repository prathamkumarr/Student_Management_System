from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column, relationship
from Backends.Shared.base import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    method_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    method_name = mapped_column(String(50), nullable=False, unique=True)  
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, default=func.now())

    payments = relationship("FeePayment", back_populates="payment_method")
    board_exam_fees = relationship("ExamFeePayment", back_populates="payment_method")