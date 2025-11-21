from sqlalchemy import Integer, String, Date, DateTime, Boolean, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base

class FeeMaster(Base):
    __tablename__ = "fees_master"

    fee_id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_id : Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    fee_type : Mapped[str] = mapped_column(String(50), nullable=False)
    amount : Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency : Mapped[str] = mapped_column(String(3), default="INR")
    effective_from : Mapped[Date] = mapped_column(Date)
    effective_to : Mapped[Date] = mapped_column(Date)
    notes : Mapped[str] = mapped_column(String(255))
    is_active : Mapped[str] = mapped_column(Boolean, default=True)
    created_at : Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now())

    # Relationships
    student_fees = relationship("StudentFee", back_populates="fees_master")
    class_ref = relationship("ClassMaster", back_populates="fees")
