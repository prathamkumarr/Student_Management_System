from sqlalchemy import Integer, String, Float, Numeric, Boolean, DateTime, func, UniqueConstraint, ForeignKey
from sqlalchemy.orm import  mapped_column
from Backends.Shared.base import Base

class StudentMarks(Base):
    __tablename__ = "student_marks"
    __table_args__ = (
        UniqueConstraint(
        "student_id",
        "subject_id",
        "exam_id",
        name="uq_student_subject_exam"
        ),
    )

    mark_id = mapped_column(Integer, primary_key=True, autoincrement=True)

    student_id = mapped_column(Integer, ForeignKey("students_master.student_id"), nullable=False)
    subject_id = mapped_column(Integer, ForeignKey("subjects_master.subject_id"), nullable=False)
    exam_id =mapped_column(Integer, ForeignKey("exams_master.exam_id"), nullable=False)

    marks_obtained = mapped_column(Numeric(6, 2))
    max_marks = mapped_column(Float, nullable=False)

    remarks = mapped_column(String(255))

    # result will be auto-calculated later (pass/fail)
    is_pass = mapped_column(Boolean, default=None)

    # Optional timestamps
    created_at = mapped_column(DateTime, server_default=func.now())
