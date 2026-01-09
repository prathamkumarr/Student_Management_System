# Backends/Shared/models/teacher_transfer_models.py
from sqlalchemy import Integer, String, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base
from sqlalchemy import Enum as SAEnum
from Backends.Shared.enums.transfer_enums import TransferStatus

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
    status = mapped_column(
        SAEnum(TransferStatus, name="teacher_transfer_status_enum"),
        default=TransferStatus.PENDING,
        nullable=False
    )
    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )
    approved_at = mapped_column(DateTime, nullable=True)
    rejected_at = mapped_column(DateTime, nullable=True)
    reject_reason = mapped_column(String(255), nullable=True)

    # relationship
    teacher = relationship("TeacherMaster", back_populates="transfer_ref")
