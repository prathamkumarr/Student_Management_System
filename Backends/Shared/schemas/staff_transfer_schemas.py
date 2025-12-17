from pydantic import BaseModel
from datetime import date

class StaffTransferCreate(BaseModel):
    staff_id: int
    new_department: str | None = None
    new_role: str | None
    request_date: date
    class Config:
        from_attributes = True

class StaffTransferResponse(BaseModel):
    transfer_id: int
    staff_id: int
    old_department: str | None
    old_role: str | None
    new_department: str | None
    new_role: str | None
    request_date: date
    status: bool
    class Config:
        from_attributes = True