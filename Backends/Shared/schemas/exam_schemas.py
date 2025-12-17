from pydantic import BaseModel
from datetime import date

class ExamCreate(BaseModel):
    exam_name: str
    description: str | None = None
    exam_date: date
    class Config:
        from_attributes = True

class ExamResponse(ExamCreate):
    exam_id: int
    is_active: bool

    class Config:
        from_attributes = True

class ExamUpdate(BaseModel):
    exam_name: str
    description: str
    exam_date: date
    class Config:
        from_attributes = True
