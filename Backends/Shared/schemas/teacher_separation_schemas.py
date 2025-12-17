from pydantic import BaseModel
from datetime import date

class TeacherSeparationCreate(BaseModel):
    teacher_id: int
    reason: str
    remarks: str | None = None
    separation_date: date

    class Config:
        from_attributes = True


class TeacherSeparationResponse(BaseModel):
    sep_id: int
    teacher_id: int
    reason: str
    remarks: str | None
    separation_date: date
    status: bool

    class Config:
        from_attributes = True
