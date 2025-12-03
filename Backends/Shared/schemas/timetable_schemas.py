from typing import Optional
from pydantic import BaseModel, Field
import datetime


class TimetableBase(BaseModel):
    class_id: int
    teacher_id: Optional[int] = None
    day: str = Field(..., max_length=20)
    subject: str = Field(..., max_length=100)
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    room_no: Optional[str] = None

    class Config:
        orm_mode = True


class TimetableCreate(TimetableBase):
    pass


class TimetableUpdate(BaseModel):
    class_id: Optional[int] = None
    teacher_id: Optional[int] = None
    day: Optional[str] = None
    subject: Optional[str] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    room_no: Optional[str] = None

    class Config:
        orm_mode = True


class TimetableOut(TimetableBase):
    timetable_id: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class TimetableFilter(BaseModel):
    class_id: Optional[int] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None
