# Backends/Backend_admin/schemas/admission_schemas.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AdmissionCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    address: str
    father_name: str
    mother_name: Optional[str] = None
    parent_phone: str
    parent_email: Optional[str] = None
    class_id: int
    previous_school: Optional[str] = None
    class Config:
        from_attributes = True


class AdmissionResponse(AdmissionCreate):
    admission_id: int
    created_at: date
    class Config:
        from_attributes = True
