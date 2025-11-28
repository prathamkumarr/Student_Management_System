from pydantic import BaseModel
from datetime import date

class TCCreate(BaseModel):
    student_id: int
    reason: str
    remarks: str | None = None
    class Config:
        from_attributes = True

class TCResponse(BaseModel):
    tc_id: int
    student_id: int
    issue_date: date
    reason: str
    remarks: str | None

    class Config:
        from_attributes = True
