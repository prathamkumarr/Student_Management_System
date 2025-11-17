from typing import Optional, Literal, Annotated, List
from datetime import date, datetime
from pydantic import BaseModel, Field

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
    status: str = Field(default="P", pattern="^(P|A|L)$")
    remarks: Optional[str] = None
    class Config:
        from_attributes = True

class MarkAttendanceBulk(BaseModel):
    items: List[MarkAttendanceItem]
    class Config:
        from_attributes = True  

class StudentAttendanceBase(BaseModel):
    student_id: PositiveInt = Field(..., description="Student ID (must exist in students_master)")
    class_id: PositiveInt = Field(..., description="Class ID (must exist in classes_master)")
    subject_id: PositiveInt = Field(..., description="Subject ID (must exist in subjects_master)")
    teacher_id: PositiveInt = Field(..., description="Teacher ID (who marks the attendance)")
    lecture_date: date = Field(..., description="Date of the lecture")
    status: str = Field(default="P", pattern="^(P|A|L)$")
    remarks: Optional[NoteStr] = Field(None, description="Optional remarks")

    class Config:
        from_attributes = True

class AttendanceOut(BaseModel):
    attendance_id: int
    student_id: int
    subject_id: int
    class_id: int
    lecture_date: date
    status: str
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
    student_id: int
    subject_id: int
    class_id: int
    lecture_date: date
    status: str = Field(pattern="^(P|A|L)$")
    remarks: Optional[str] = None
    class Config:
        from_attributes = True  

class StudentAttendanceResponse(StudentAttendanceBase):
    attendance_id: int
    student_name: Optional[str] = None
    subject_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ---------- Teacher attendance schemas ----------
class TeacherAttendanceBase(BaseModel):
    teacher_id: PositiveInt = Field(..., description="Teacher ID (must exist in teachers_master)")
    on_date: date = Field(..., description="Attendance date (use `on_date` to avoid shadowing)")
    check_in: Optional[datetime] = Field(None, description="Time teacher checked in")
    check_out: Optional[datetime] = Field(None, description="Time teacher checked out")
    status: str = Field(default="P", pattern="^(P|A|L)$")
    remarks: Optional[NoteStr] = Field(None, description="Optional remarks about attendance")
    class Config:
        from_attributes = True

class TeacherAttendanceCreate(TeacherAttendanceBase):
    pass

class TeacherAttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    status: Optional[Literal["P", "A", "L"]] = None
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

class TeacherAttendanceResponse(TeacherAttendanceBase):
    record_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ---------- Filters & Lists (admin/search helpers) ----------
class AttendanceFilter(BaseModel):
    on_date: Optional[date] = Field(None, description="Filter by specific date")
    student_ids: Optional[List[int]] = Field(None, description="Filter by list of student IDs")
    class_ids: Optional[List[int]] = Field(None, description="Filter by list of class IDs")
    subject_ids: Optional[List[int]] = Field(None, description="Filter by list of subject IDs")
    teacher_ids: Optional[List[int]] = Field(None, description="Filter by list of teacher IDs")
    status: Optional[Literal["Present", "Absent", "Leave"]] = Field(None, description="Filter by status")
    limit: Optional[int] = Field(100, description="Max records to return")
    offset: Optional[int] = Field(0, description="Pagination offset")
    class Config:
        from_attributes = True


class AttendanceListResponse(BaseModel):
    items: List[StudentAttendanceResponse]
    total: int
    class Config:
        from_attributes = True
