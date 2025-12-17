from sqlalchemy import Integer, String, Date, Boolean
from sqlalchemy.orm import  mapped_column
from Backends.Shared.base import Base

class ExamMaster(Base):
    __tablename__ = "exams_master"

    exam_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    exam_name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(255))
    exam_date = mapped_column(Date, nullable=False)
    is_active = mapped_column(Boolean, default=True)
