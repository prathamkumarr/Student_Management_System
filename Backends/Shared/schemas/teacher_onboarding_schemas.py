# Backends/Shared/schemas/teacher_onboarding_schemas.py

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class TeacherOnboardingCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    address: str
    email: str
    phone: str
    subject_id: int
    qualification: Optional[str] = None
    experience_years: Optional[int] = 0

    class Config:
        from_attributes = True


class TeacherOnboardingResponse(TeacherOnboardingCreate):
    onboarding_id: int
    created_at: datetime

    class Config:
        from_attributes = True
