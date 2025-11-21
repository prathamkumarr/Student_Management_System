from sqlalchemy import Integer, String, Date, DateTime, Enum, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base

class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"
    __table_args__ = (
            UniqueConstraint("teacher_id", "date", name="uq_teacher_date"),
        )

    record_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers_master.teacher_id"), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    check_in: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    check_out: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(Enum("P", "A", "L", name="teacher_attendance_status"), nullable=False)
    remarks: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now())

    # relationships
    teacher = relationship("TeacherMaster", back_populates="teacher_attendance_records")
