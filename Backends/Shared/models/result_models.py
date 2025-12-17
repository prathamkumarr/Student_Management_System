from sqlalchemy import Integer, String, Float, DateTime, func
from sqlalchemy.orm import  mapped_column
from Backends.Shared.base import Base

class ResultMaster(Base):
    __tablename__ = "results_master"

    result_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id = mapped_column(Integer, nullable=False)
    exam_id = mapped_column(Integer, nullable=False)

    total_marks = mapped_column(Float, nullable=False)
    obtained_marks = mapped_column(Float, nullable=False)
    percentage = mapped_column(Float, nullable=False)
    grade = mapped_column(String(5))

    result_status = mapped_column(String(10))  # PASS / FAIL

    generated_at = mapped_column(DateTime, server_default=func.now())
