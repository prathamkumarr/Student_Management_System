# Backends/Shared/schemas/teacher_onboarding_schemas.py

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from Backends.Shared.enums.gender_enums import GenderEnum
from Backends.Shared.enums. teacher_onboarding_enums import TeacherOnboardingStatus

class TeacherOnboardingCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    email: str
    phone: str
    subject_id: int
    qualification: Optional[str] = None
    experience_years: Optional[int] = 0
    approved_at: datetime | None = None
    rejected_at: datetime | None = None
    reject_reason: str | None = None
    status: TeacherOnboardingStatus

    class Config:
        from_attributes = True


class TeacherOnboardingResponse(TeacherOnboardingCreate):
    onboarding_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TeacherOnboardingReject(BaseModel):
    reason: str

    class Config:
        from_attributes = True