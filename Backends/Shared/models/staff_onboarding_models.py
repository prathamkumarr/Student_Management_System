# Backends/Shared/models/staff_onboarding_models.py

from sqlalchemy import Integer, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SAEnum
from Backends.Shared.base import Base
from Backends.Shared.enums.staff_onboarding_enums import StaffOnboardingStatus
from Backends.Shared.enums.gender_enums import GenderEnum

class StaffOnboarding(Base):
    __tablename__ = "staff_onboarding"

    onboarding_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        SAEnum(GenderEnum, name="gender_enum"),
        nullable=False
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    status: Mapped[StaffOnboardingStatus] = mapped_column(
        SAEnum(StaffOnboardingStatus, name="staff_onboarding_status"),
        default=StaffOnboardingStatus.PENDING,
        nullable=False)
    
    # Job details
    department: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(120), nullable=False)

    experience_years: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    approved_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    rejected_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    reject_reason = mapped_column(String(255), nullable=True)