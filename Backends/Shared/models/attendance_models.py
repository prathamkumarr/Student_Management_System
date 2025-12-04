# Backends/models/attendance_models.py
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, Date, DateTime, BigInteger, func, ForeignKey, UniqueConstraint, Boolean
from Backends.Shared.base import Base
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.subjects_master import SubjectMaster
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.teachers_master import TeacherMaster

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", "lecture_date", name="uq_att_unique"),
    )

    attendance_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students_master.student_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects_master.subject_id"), nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers_master.teacher_id"), nullable=False)
    
    lecture_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(Enum("P", "A", "L"))
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active = mapped_column(Boolean, default=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now())

    student_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    subject_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # relationships
    student: Mapped["StudentMaster"] = relationship("StudentMaster", back_populates="attendance_records")
    subject: Mapped[list["SubjectMaster"]] = relationship("SubjectMaster", back_populates="attendance_records")
    class_ref: Mapped[list["ClassMaster"]] = relationship("ClassMaster", back_populates="attendance_records")
    teacher: Mapped[list["TeacherMaster"]] = relationship("TeacherMaster", back_populates="student_attendance_records")

    
