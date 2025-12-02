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
    due_date: Optional[date] = None

    class Config:
        orm_mode = True


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
    file_path: Optional[str] = None

    class Config:
        orm_mode = True


class WorkOut(WorkBase):
    work_id: int
    file_path: str
    created_at: datetime
    updated_at: datetime
