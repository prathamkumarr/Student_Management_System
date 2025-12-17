# Backends/Shared/models/teacher_onboarding_models.py

from sqlalchemy import Integer, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class TeacherOnboarding(Base):
    __tablename__ = "teacher_onboarding"

    onboarding_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # personal details
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    
    # job details
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    qualification: Mapped[str] = mapped_column(String(120), nullable=True)
    experience_years: Mapped[int] = mapped_column(Integer, default=0)

    # meta
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
