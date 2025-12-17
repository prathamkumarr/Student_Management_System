# Backends/Shared/schemas/teacher_transfer_schemas.py
from pydantic import BaseModel
from datetime import date

class TeacherTransferCreate(BaseModel):
    teacher_id: int
    new_department: str | None = None
    new_subject_id: int | None = None
    new_class_id:int | None
    request_date: date

    class Config:
        from_attributes = True

class TeacherTransferResponse(BaseModel):
    transfer_id: int
    teacher_id: int
    old_department: str | None
    old_subject_id: int | None
    old_class_id:int | None
    new_department: str | None
    new_subject_id: int | None
    new_class_id:int | None
    request_date: date
    status: bool

    class Config:
        from_attributes = True
