from pydantic import BaseModel
from datetime import date
from datetime import datetime
from Backends.Shared.enums.transfer_enums import TransferStatus

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
    status: TransferStatus
    approved_at: datetime | None
    rejected_at: datetime | None
    reject_reason: str | None

    class Config:
        from_attributes = True

class RejectTransferRequest(BaseModel):
    reason: str
    class Config:
        from_attributes = True        