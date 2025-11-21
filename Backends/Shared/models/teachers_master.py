from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base
from Backends.Shared.models.teacher_attendance_models import TeacherAttendance

class TeacherMaster(Base):
    __tablename__ = "teachers_master"

    teacher_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(120))
    subject_id: Mapped[int] = mapped_column(Integer)  # can add FK later if you want
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)

    # relationships
    student_attendance_records = relationship("AttendanceRecord", back_populates="teacher")
    teacher_attendance_records: Mapped["TeacherAttendance"] = relationship("TeacherAttendance", back_populates="teacher")
