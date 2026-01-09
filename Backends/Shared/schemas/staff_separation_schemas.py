from pydantic import BaseModel
from datetime import date
from datetime import date, datetime
from Backends.Shared.enums.separation_enums import SeparationStatus

class StaffSeparationCreate(BaseModel):
    staff_id: int
    reason: str
    remarks: str | None = None
    separation_date: date
    class Config:
        from_attributes = True


class StaffSeparationResponse(BaseModel):
    sep_id: int
    staff_id: int
    reason: str
    remarks: str | None
    separation_date: date
    status: SeparationStatus
    approved_at: datetime | None
    rejected_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True

class RejectRequest(BaseModel):
    reason: str
    class Config:
        from_attributes = True