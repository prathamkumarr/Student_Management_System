from pydantic import BaseModel
from datetime import date

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
    status: bool
    class Config:
        from_attributes = True
