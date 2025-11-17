# fees_models.py
from sqlalchemy import (
    Integer, String, DECIMAL, Date, DateTime,
    Enum, ForeignKey, JSON, func
)
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.payment_method import PaymentMethod


# Student Fees – invoice / due records
class StudentFee(Base):
    __tablename__ = "student_fees"

    invoice_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students_master.student_id"), nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    fee_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("fees_master.fee_id"), nullable=True)

    amount_due: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    amount_paid: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.00)
    due_date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(Enum("pending", "partially_paid", "paid", "cancelled", name="fee_status_enum"), default="pending")

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    receipt_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    student_ref: Mapped[list["StudentMaster"]] = relationship("StudentMaster", back_populates="student_fees")
    class_ref: Mapped[list["ClassMaster"]] = relationship("ClassMaster", back_populates="student_fees")
    fees_master: Mapped[list["FeeMaster"]] = relationship("FeeMaster", back_populates="student_fees")
    payments: Mapped[list["FeePayment"]] = relationship("FeePayment", back_populates="invoice_ref")
    audits: Mapped[list["FeeAudit"]]= relationship("FeeAudit", back_populates="invoice_ref")


# Fee Payments – actual transactions
class FeePayment(Base):
    __tablename__ = "fee_payments"

    payment_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id = mapped_column(Integer, ForeignKey("student_fees.invoice_id"))
    student_id = mapped_column(Integer)
    amount = mapped_column(DECIMAL(10,2))
    payment_method_id = mapped_column(Integer, ForeignKey("payment_methods.method_id"))

    status = mapped_column(String(20), default="success")
    created_at = mapped_column(DateTime, default=func.now())

    # relationships
    invoice_ref: Mapped[list["StudentFee"]] = relationship("StudentFee", back_populates="payments")
    payment_method: Mapped[list["PaymentMethod"]] = relationship("PaymentMethod", back_populates="payments")

# Fee Audit – changes in invoices or payments
class FeeAudit(Base):
    __tablename__ = "fee_audit"

    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(Integer, ForeignKey("student_fees.invoice_id"), nullable=False)
    changed_by: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    before_change: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_change: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ts: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # relationships
    invoice_ref: Mapped[list["StudentFee"]]= relationship("StudentFee", back_populates="audits")

class ExamFeePayment(Base):
    __tablename__ = "exam_fee_payments"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exam_fee_id: Mapped[int] = mapped_column(ForeignKey("exam_fee_master.exam_fee_id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students_master.student_id"))
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.method_id"))
    status: Mapped[str] = mapped_column(String(20), default="success")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    payment_method: Mapped[list["PaymentMethod"]] = relationship("PaymentMethod", back_populates="board_exam_fees")
    student: Mapped[list["StudentMaster"]] = relationship("StudentMaster", back_populates="exam_fees")
