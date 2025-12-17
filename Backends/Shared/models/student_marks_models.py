from sqlalchemy import Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import  mapped_column
from Backends.Shared.base import Base

class StudentMarks(Base):
    __tablename__ = "student_marks"

    mark_id = mapped_column(Integer, primary_key=True, autoincrement=True)

    student_id = mapped_column(Integer, nullable=False)
    subject_id = mapped_column(Integer, nullable=False)
    exam_id =mapped_column(Integer, nullable=False)

    marks_obtained = mapped_column(Float, nullable=False)
    max_marks = mapped_column(Float, nullable=False)

    remarks = mapped_column(String(255))

    # result will be auto-calculated later (pass/fail)
    is_pass = mapped_column(Boolean, default=None)

    # Optional timestamps
    created_at = mapped_column(DateTime, server_default=func.now())
