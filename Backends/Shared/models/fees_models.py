# fees_models.py
from sqlalchemy import (
    Integer, String, DECIMAL, Date, DateTime,
    Enum, ForeignKey, JSON, func, Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base
from decimal import Decimal
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus
from Backends.Shared.enums.fee_payments_enums import (
    FeePaymentStatus,
    PaymentSource,
    PaymentReceivedBy
)
from Backends.Shared.enums.fees_enums import (
    BillingType,
    FeeFrequency,
    ChargeTrigger,
    FeeGeneratedBy
)
from Backends.Shared.enums.fee_audit_enums import (
    FeeAuditEntity,
    FeeAuditAction,
    AuditActorRole,
    AuditSource
)



# ==============================================================
# Student Fees – invoice / due records
class StudentFee(Base):
    __tablename__ = "student_fees"
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "fee_id",
            "due_date",
            name="uq_student_fee_cycle"
        ),
    )

    invoice_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students_master.student_id"), nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    fee_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("fees_master.fee_id"), nullable=True)

    amount_due: Mapped[Decimal] = mapped_column(DECIMAL(10,2), nullable=False)
    amount_paid: Mapped[Decimal] = mapped_column(DECIMAL(10,2), default=Decimal("0.00"), nullable=False)

    due_date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[StudentFeeStatus] = mapped_column(
        Enum(StudentFeeStatus),
        default=StudentFeeStatus.PENDING,
        nullable=False
        )
    billing_type: Mapped[BillingType] = mapped_column(
        Enum(BillingType),
        nullable=False
        )   
    frequency: Mapped[FeeFrequency | None] = mapped_column(
        Enum(FeeFrequency),
        nullable=True
        )
    charge_trigger: Mapped[ChargeTrigger] = mapped_column(
        Enum(ChargeTrigger),
        nullable=False
        )
    billing_period_start: Mapped[Date | None] = mapped_column(Date, nullable=True)
    billing_period_end: Mapped[Date | None] = mapped_column(Date, nullable=True)

    is_active = mapped_column(Boolean, default=True)
    
    generated_by: Mapped[FeeGeneratedBy] = mapped_column(
        Enum(FeeGeneratedBy),
        default=FeeGeneratedBy.SYSTEM,
        nullable=False
        )

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    student_ref = relationship("StudentMaster", back_populates="student_fees")

    class_ref = relationship("ClassMaster", back_populates="student_fees")
    fees_master = relationship("FeeMaster", back_populates="student_fees")
    payments: Mapped[list["FeePayment"]] = relationship("FeePayment", back_populates="invoice_ref")
    audits: Mapped[list["FeeAudit"]]= relationship("FeeAudit", back_populates="invoice_ref")



# ===============================================================
# Fee Payments – actual transactions
class FeePayment(Base):
    __tablename__ = "fee_payments"

    payment_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id = mapped_column(Integer, ForeignKey("student_fees.invoice_id"))
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students_master.student_id"),
        nullable=False
        )

    amount = mapped_column(DECIMAL(10,2))
    payment_method_id = mapped_column(Integer, ForeignKey("payment_methods.method_id"))
    payment_method_name: Mapped[str] = mapped_column(String(50))
    
    payer_id = mapped_column(Integer, nullable=True)
    payer_role = mapped_column(String(20))  # student / parent / admin
    
    payment_provider: Mapped[str | None] = mapped_column(String(50), default="gateway")
    provider_txn_id: Mapped[str | None] = mapped_column(String(100))
    response_payload: Mapped[dict | None] = mapped_column(JSON)

    status = mapped_column(
        Enum(FeePaymentStatus),
        default=FeePaymentStatus.SUCCESS,
        nullable=False
    )
    payment_source: Mapped[PaymentSource] = mapped_column(
        Enum(PaymentSource),
        nullable=False
        )
    billing_cycle: Mapped[Date | None] = mapped_column(Date, nullable=True)
    is_partial_payment: Mapped[bool] = mapped_column(Boolean, default=False)
    received_by: Mapped[PaymentReceivedBy] = mapped_column(
    Enum(PaymentReceivedBy),
    default=PaymentReceivedBy.ONLINE
    )
    remarks: Mapped[str | None] = mapped_column(String(255))

    created_at = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        onupdate=func.now()
        )

    # relationships
    invoice_ref: Mapped[list["StudentFee"]] = relationship("StudentFee", back_populates="payments")
    payment_method_rel = relationship("PaymentMethod", back_populates="payments")



# ===============================================================
# Fee Audit – changes in invoices or payments
class FeeAudit(Base):
    __tablename__ = "fee_audit"

    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(Integer, ForeignKey("student_fees.invoice_id"), nullable=False)
    changed_by: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    before_change: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_change: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    entity_type: Mapped[FeeAuditEntity] = mapped_column(
    Enum(FeeAuditEntity),
    nullable=False
    ) 
    action: Mapped[FeeAuditAction] = mapped_column(
    Enum(FeeAuditAction),
    nullable=False
    )
    changed_by_role: Mapped[AuditActorRole] = mapped_column(
    Enum(AuditActorRole),
    nullable=False
    )
    reason: Mapped[str | None] = mapped_column(String(255))
    source: Mapped[AuditSource] = mapped_column(
    Enum(AuditSource),
    default=AuditSource.UI
    )

    ts: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # relationships
    invoice_ref: Mapped[list["StudentFee"]]= relationship("StudentFee", back_populates="audits")
