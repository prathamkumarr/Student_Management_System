from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from Backends.Shared.enums.gender_enums import GenderEnum
from Backends.Shared.enums. staff_onboarding_enums import StaffOnboardingStatus

class StaffOnboardingCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    email: str
    phone: str
    department: str
    role: str
    experience_years: Optional[int] = 0
    approved_at: datetime | None = None
    rejected_at: datetime | None = None
    reject_reason: str | None = None
    status: StaffOnboardingStatus

    class Config:
        from_attributes = True


class StaffOnboardingResponse(StaffOnboardingCreate):
    onboarding_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class StaffOnboardingReject(BaseModel):
    reason: str

    class Config:
        from_attributes = True