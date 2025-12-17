from sqlalchemy import Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, relationship
from Backends.Shared.base import Base

class TeacherSeparation(Base):
    __tablename__ = "teacher_separation"

    sep_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    teacher_id = mapped_column(Integer, ForeignKey("teachers_master.teacher_id"), nullable=False)
    reason = mapped_column(String(255), nullable=False)
    remarks = mapped_column(String(255))
    separation_date = mapped_column(Date, nullable=False)
    status = mapped_column(Boolean, default=False)  # False = Pending, True = Approved

    teacher = relationship("TeacherMaster", back_populates="separation_ref")
