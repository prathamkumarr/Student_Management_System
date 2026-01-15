# Backends/Backend_students/routers/attendance_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from Backends.Shared.connection import get_db
from Backends.Shared.models.attendance_models import AttendanceRecord
from Backends.Shared.schemas.attendance_schemas import (
    AttendanceFilter, AttendanceOut, AttendanceSummary
    )
from Backends.Shared.enums.attendance_enums import AttendanceStatus
from Backends.Shared.models.students_master import StudentMaster

router = APIRouter(prefix="/student/attendance", tags=["Attendance"])

# endpoint to fetch student's attendance by date filter
@router.post("/by-date", response_model=List[AttendanceOut])
def get_by_student(filter: AttendanceFilter, db: Session = Depends(get_db)):
    q = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == filter.student_id,
        AttendanceRecord.lecture_date.between(
            filter.date_from, filter.date_to
        ),
        AttendanceRecord.is_active == True
    )

    if filter.subject_id:
        q = q.filter(AttendanceRecord.subject_id == filter.subject_id)

    return q.order_by(AttendanceRecord.lecture_date).all()


# endpoint to see summary of attendance of a student using filters
@router.get("/summary/{student_id}", response_model=AttendanceSummary)
def summary(
    student_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db)
):
    # ---- validate student ----
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(404, "Student not found")

    if date_from > date_to:
        raise HTTPException(400, "date_from cannot be after date_to")

    q = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.lecture_date.between(date_from, date_to)
    )

    total = q.count()
    if total == 0:
        raise HTTPException(404, "No attendance records found")

    present = q.filter(AttendanceRecord.status == AttendanceStatus.P).count()
    absent  = q.filter(AttendanceRecord.status == AttendanceStatus.A).count()
    late    = q.filter(AttendanceRecord.status == AttendanceStatus.L).count()
    leave    = q.filter(AttendanceRecord.status == AttendanceStatus.LE).count()

    percentage = round((present / total) * 100, 2)

    return AttendanceSummary(
        student_id=student_id,
        total_lectures=total,
        present=present,
        absent=absent,
        late=late,
        leave=leave,
        percentage=percentage
    )

