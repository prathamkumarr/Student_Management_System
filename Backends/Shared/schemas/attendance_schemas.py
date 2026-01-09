from typing import Optional, Literal, Annotated, List
from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List
from Backends.Shared.enums.attendance_enums import AttendanceStatus

# ---- helpers ----
PositiveInt = Annotated[int, Field(gt=0)]
Money = Annotated[float, Field(max_digits=12, decimal_places=2)]
NoteStr = Annotated[str, Field(max_length=255)]


# ---- Student attendance schemas ---
class MarkAttendanceItem(BaseModel):
    student_id: int
    subject_id: int
    class_id: int
    lecture_date: date
    status: AttendanceStatus = AttendanceStatus.P
    remarks: Optional[str] = None
    class Config:
        from_attributes = True

class MarkAttendanceBulk(BaseModel):
    class_id: int
    subject_id: int
    lecture_date: date
    absent_ids: List[int]
    class Config:
        from_attributes = True

class StudentAttendanceBase(BaseModel):
    student_id: PositiveInt = Field(..., description="Student ID (must exist in students_master)")
    class_id: PositiveInt = Field(..., description="Class ID (must exist in classes_master)")
    subject_id: PositiveInt = Field(..., description="Subject ID (must exist in subjects_master)")
    teacher_id: int | None   
    lecture_date: date = Field(..., description="Date of the lecture")
    status: AttendanceStatus = AttendanceStatus.P
    remarks: Optional[NoteStr] = Field(None, description="Optional remarks")

    class Config:
        from_attributes = True

class AttendanceOut(BaseModel):
    attendance_id: int
    student_id: int
    subject_id: int
    class_id: int
    lecture_date: date
    status: AttendanceStatus
    remarks: Optional[str] = None
    class Config:
        from_attributes = True  

class AttendanceSummary(BaseModel):
    student_id: int
    total_lectures: int
    present: int
    absent: int
    late: int
    percentage: float
    class Config:
        from_attributes = True  

class StudentAttendanceCreate(StudentAttendanceBase):
    pass

class UpdateAttendanceItem(BaseModel):
    status: AttendanceStatus = AttendanceStatus.P
    remarks: Optional[str] = None
    class Config:
        from_attributes = True  

class StudentAttendanceResponse(StudentAttendanceBase):
    attendance_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ---------- Teacher attendance schemas ----------
class TeacherAttendanceBase(BaseModel):
    teacher_id: PositiveInt
    date: date       
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: AttendanceStatus = AttendanceStatus.P
    remarks: Optional[NoteStr] = None
    class Config:
        from_attributes = True

class TeacherAttendanceCreate(TeacherAttendanceBase):
    pass

class TeacherAttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    status: Optional[AttendanceStatus] = None
    remarks: Optional[str] = None
    class Config:
        from_attributes = True

class TeacherAttendanceSummary(BaseModel):
    teacher_id: int
    total_days: int
    present: int
    absent: int
    leave: int
    percentage: float
    class Config:
        from_attributes = True

class TeacherAttendanceResponse(BaseModel):
    record_id: int
    teacher_id: int
    date: date
    check_in: datetime | None
    check_out: datetime | None
    status: AttendanceStatus
    remarks: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# ---------- Filters & Lists (admin/search helpers) ----------
class AttendanceFilter(BaseModel):
    student_id: int
    date_from: date
    date_to: date
    subject_id: Optional[int] = None
    class Config:
        from_attributes = True


class AttendanceListResponse(BaseModel):
    items: List[StudentAttendanceResponse]
    total: int
    class Config:
        from_attributes = True


# ---------- Staff attendance schemas ----------
class StaffAttendanceBase(BaseModel):
    staff_id: PositiveInt
    date: date       
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: AttendanceStatus = AttendanceStatus.P
    remarks: Optional[NoteStr] = None
    class Config:
        from_attributes = True

class StaffAttendanceCreate(StaffAttendanceBase):
    pass

class StaffAttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    status: Optional[AttendanceStatus] = None
    remarks: Optional[str] = None
    class Config:
        from_attributes = True

class StaffAttendanceSummary(BaseModel):
    staff_id: int
    total_days: int
    present: int
    absent: int
    leave: int
    percentage: float
    class Config:
        from_attributes = True

class StaffAttendanceResponse(BaseModel):
    record_id: int
    staff_id: int
    date: date
    check_in: datetime | None
    check_out: datetime | None
    status: AttendanceStatus
    remarks: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True