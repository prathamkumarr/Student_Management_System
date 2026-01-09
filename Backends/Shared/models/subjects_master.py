from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class SubjectMaster(Base):
    __tablename__ = "subjects_master"

    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # relationships
    attendance_records = relationship("AttendanceRecord", back_populates="subject")
    teachers = relationship("TeacherOnboarding", back_populates="subject")

