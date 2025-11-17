# Backends/Backend_students/routers/attendance_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from sqlalchemy import text
from datetime import datetime

from Backends.Shared.connection import get_db
from Backends.Backend_students.models.attendance_models import AttendanceRecord
from Backends.Backend_admin.schemas.attendance_schemas import (
    AttendanceFilter, AttendanceOut, AttendanceSummary
    )

router = APIRouter(prefix="/student/attendance", tags=["Attendance"])

# endpoint to fetch student's attendance by date filter
@router.post("/by-student", response_model=List[AttendanceOut])
def get_by_student(filter: AttendanceFilter, db: Session = Depends(get_db)):
    q = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == filter.student_id,
        AttendanceRecord.lecture_date.between(filter.date_from, filter.date_to)
    )
    if filter.subject_id:
        q = q.filter(AttendanceRecord.subject_id == filter.subject_id)
    recs = q.order_by(AttendanceRecord.lecture_date.asc()).all()

    return [
        AttendanceOut(
            attendance_id=r.attendance_id,
            student_id=r.student_id,
            subject_id=r.subject_id,
            class_id=r.class_id,
            lecture_date=r.lecture_date,
            status=r.status,
            remarks=r.remarks
        )
        for r in recs
    ]

# endpoint to see summary of attendance of a student using filters
@router.get("/summary/{student_id}", response_model=AttendanceSummary)
def summary(student_id: int, date_from: date, date_to: date, db: Session = Depends(get_db)):
    q = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.lecture_date.between(date_from, date_to)
    )
    total = q.count()
    present = q.filter(AttendanceRecord.status == "P").count()
    absent = q.filter(AttendanceRecord.status == "A").count()
    late = q.filter(AttendanceRecord.status == "L").count()
    percentage = round((present / total) * 100, 2) if total else 0.0

    return AttendanceSummary(
        student_id=student_id,
        total_lectures=total,
        present=present,
        absent=absent,
        late=late,
        percentage=percentage
    )

