# Backends/Shared/schemas/staff_onboarding_schemas.py

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class StaffOnboardingCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    address: str
    email: str
    phone: str
    department: str
    role: str
    experience_years: Optional[int] = 0

    class Config:
        from_attributes = True


class StaffOnboardingResponse(StaffOnboardingCreate):
    onboarding_id: int
    created_at: datetime

    class Config:
        from_attributes = True
