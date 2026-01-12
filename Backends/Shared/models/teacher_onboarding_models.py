# Backends/Shared/models/teacher_onboarding_models.py

from sqlalchemy import Integer, String, Date, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from Backends.Shared.base import Base
from Backends.Shared.enums.teacher_onboarding_enums import TeacherOnboardingStatus
from Backends.Shared.enums.gender_enums import GenderEnum

class TeacherOnboarding(Base):
    __tablename__ = "teacher_onboarding"

    onboarding_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # personal details
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        SAEnum(GenderEnum, name="gender_enum"),
        nullable=False
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    status: Mapped[TeacherOnboardingStatus] = mapped_column(
        SAEnum(TeacherOnboardingStatus, name="teacher_onboarding_status"),
        default=TeacherOnboardingStatus.PENDING,
        nullable=False)
    
    # job details
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects_master.subject_id"), nullable=False)
    qualification: Mapped[str] = mapped_column(String(120), nullable=True)
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    academic_session_id = mapped_column(
        Integer,
        ForeignKey("academic_session.session_id"),
        nullable=False,
        index=True
    )

    # meta
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    approved_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    rejected_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    reject_reason = mapped_column(String(255), nullable=True)

    # relationships
    subject = relationship("SubjectMaster", back_populates="teachers")

