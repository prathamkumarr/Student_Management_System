# Backends/Shared/models/teacher_transfer_models.py
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base


class TeacherTransfer(Base):
    __tablename__ = "teacher_transfers"

    transfer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    teacher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teachers_master.teacher_id"), nullable=False
    )

    # Previous (old) details
    old_department: Mapped[str] = mapped_column(String(120))
    old_subject_id: Mapped[int] = mapped_column(Integer, nullable=True)
    old_class_id: Mapped[int] = mapped_column(Integer, nullable=True)

    # Updated (new) details
    new_department: Mapped[str] = mapped_column(String(120), nullable=True)
    new_subject_id: Mapped[int] = mapped_column(Integer, nullable=True)
    new_class_id: Mapped[int] = mapped_column(Integer, nullable=True)

    request_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[bool] = mapped_column(default=False)   

    teacher = relationship("TeacherMaster", back_populates="transfer_ref")
