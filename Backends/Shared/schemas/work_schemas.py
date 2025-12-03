from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field


class WorkBase(BaseModel):
    class_id: int
    teacher_id: Optional[int] = None
    subject: str = Field(..., max_length=100)
    work_type: str = Field(..., max_length=20)
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    due_date: Optional[date] = None  # must be YYYY-MM-DD

    class Config:
        from_attributes = True


class WorkCreate(WorkBase):
    pass


class WorkUpdate(BaseModel):
    class_id: Optional[int] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None
    work_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None

    class Config:
        from_attributes = True


class WorkOut(WorkBase):
    work_id: int
    file_path: str
    created_at: datetime
    updated_at: datetime

    # ✅ Add missing fields so FastAPI returns them
    class_name: Optional[str] = None
    section: Optional[str] = None      # <--- Added
    teacher_name: Optional[str] = None

    class Config:
        from_attributes = True


class WorkFilter(BaseModel):
    class_id: Optional[int] = None
    class_name: Optional[str] = None
    section: Optional[str] = None
    teacher_id: Optional[int] = None
    teacher_name: Optional[str] = None
    subject: Optional[str] = None
    work_type: Optional[str] = None

    class Config:
        from_attributes = True
