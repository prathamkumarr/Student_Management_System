from sqlalchemy import Integer, String, Date, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from Backends.Shared.base import Base

class ExamFeeMaster(Base):
    __tablename__ = "exam_fee_master"

    exam_fee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes_master.class_id"))
    exam_type: Mapped[str] = mapped_column(String(50))
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    effective_from: Mapped[date] = mapped_column(Date)
    effective_to: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    class_ref = relationship("ClassMaster", back_populates="exam_fee")
