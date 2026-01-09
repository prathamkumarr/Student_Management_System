# Backends/Backend_admin/schemas/admission_schemas.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from Backends.Shared.enums.admission_enums import AdmissionStatus
from Backends.Shared.enums.gender_enums import GenderEnum

class AdmissionCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: GenderEnum
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
    status: AdmissionStatus
    student_id: Optional[int] = None

    submitted_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    remarks: Optional[str] = None

    class Config:
        from_attributes = True


class AdmissionSubmit(BaseModel):
    pass


class AdmissionVerify(BaseModel):
    remarks: Optional[str] = None


class AdmissionReject(BaseModel):
    remarks: str
