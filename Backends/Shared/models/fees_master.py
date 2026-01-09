from sqlalchemy import Integer, String, Date, DateTime, Boolean, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base
from Backends.Shared.enums.fees_enums import (
    BillingType,
    FeeFrequency,
    ChargeTrigger
)
from sqlalchemy import Enum as SAEnum


class FeeMaster(Base):
    __tablename__ = "fees_master"

    fee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("classes_master.class_id"), nullable=False
    )

    fee_type: Mapped[str] = mapped_column(String(50), nullable=False)
    billing_type: Mapped[BillingType] = mapped_column(
        SAEnum(BillingType),
        nullable=False
        )

    frequency: Mapped[FeeFrequency | None] = mapped_column(
        SAEnum(FeeFrequency),
        nullable=True
        )

    charge_trigger: Mapped[ChargeTrigger] = mapped_column(
        SAEnum(ChargeTrigger),
        default=ChargeTrigger.ACADEMIC_CYCLE,
        nullable=False
        )

    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")

    allow_proration: Mapped[bool] = mapped_column(Boolean, default=False)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)

    effective_from: Mapped[Date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[Date | None] = mapped_column(Date, nullable=True)

    notes: Mapped[str] = mapped_column(String(255))
    display_order: Mapped[int] = mapped_column(Integer, default=1)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, onupdate=func.now()
    )

    student_fees = relationship("StudentFee", back_populates="fees_master")
    class_ref = relationship("ClassMaster", back_populates="fees")
