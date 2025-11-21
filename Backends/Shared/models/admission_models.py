# Backends/Backend_admin/models/admission_models.py
from sqlalchemy import Integer, String, Date, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class StudentAdmission(Base):
    __tablename__ = "student_admissions"

    admission_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Student Personal Details
    full_name: Mapped[int] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    # Parent Details
    father_name: Mapped[str] = mapped_column(String(120), nullable=False)
    mother_name: Mapped[str] = mapped_column(String(120), nullable=True)
    parent_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    parent_email: Mapped[str] = mapped_column(String(120), nullable=True)

    # Academic Details
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    previous_school: Mapped[str] = mapped_column(String(255), nullable=True)

    # Meta
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # relationships
    class_ref = relationship(
        "ClassMaster",
        back_populates="admissions"
    )
