from pydantic import BaseModel
from datetime import date

class TCCreate(BaseModel):
    student_id: int
    reason: str
    remarks: str | None = None
    issue_date: date

    class Config:
        from_attributes = True


class TCResponse(BaseModel):
    tc_id: int
    student_id: int
    issue_date: date
    reason: str
    remarks: str | None
    is_active: bool

    class Config:
        from_attributes = True
