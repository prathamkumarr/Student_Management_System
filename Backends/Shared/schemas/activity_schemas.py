from pydantic import BaseModel
from typing import Optional

class ActivityCreate(BaseModel):
    activity_name: str
    category: Optional[str] = None
    description: Optional[str] = None
    incharge_teacher_id: Optional[int] = None

class ActivityUpdate(BaseModel):
    activity_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    incharge_teacher_id: Optional[int] = None

class ActivityOut(BaseModel):
    activity_id: int
    activity_name: str
    category: Optional[str]
    description: Optional[str]
    incharge_teacher_id: Optional[int]

    class Config:
        from_attributes = True   # Pydantic v2
