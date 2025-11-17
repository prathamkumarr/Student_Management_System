from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from datetime import date
from typing import List
# Schemas
from Backends.Backend_admin.schemas.attendance_schemas import (
    StudentAttendanceCreate, AttendanceSummary, AttendanceOut,
    StudentAttendanceResponse, AttendanceFilter,
    TeacherAttendanceCreate, TeacherAttendanceSummary,
    TeacherAttendanceResponse,
)
# Models
from Backends.Backend_teachers.models.attendance_models import TeacherAttendance
from Backends.Backend_students.models.attendance_models import AttendanceRecord

router = APIRouter(prefix="/attendance", tags=["Admin Attendance"])

# -----STUDENT ATTENDANCE-----
# endpoint to view all student's attendance 
@router.get("/student", response_model=list[StudentAttendanceResponse])
def get_all_student_attendance(db: Session = Depends(get_db)):
    return db.query(AttendanceRecord).all()

# endpoint to view attendance of a student using attendance_id
@router.get("/student/{attendance_id}", response_model=StudentAttendanceResponse)
def get_student_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance record not found")
    return record

# endpoint to view student's attendance records(using date filters)
@router.post("/student/by-student", response_model=List[AttendanceOut])
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
@router.get("/student/summary/{student_id}", response_model=AttendanceSummary)
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

# endpoint to update any students attendance using attendance_id 
@router.put("/student/{attendance_id}", response_model=StudentAttendanceResponse)
def update_student_attendance(attendance_id: int, payload: StudentAttendanceCreate, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance not found")

    for key, value in payload.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

# endpoint to delete attendance of any student using attendance_id
@router.delete("/student/{attendance_id}")
def delete_student_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Student attendance not found")

    db.delete(record)
    db.commit()
    return {"message": "Student attendance deleted"}


# -----TEACHER ATTENDANCE----- 
# endpoint to view teachers attendance
@router.get("/teacher", response_model=list[TeacherAttendanceResponse])
def get_all_teacher_attendance(db: Session = Depends(get_db)):
    return db.query(TeacherAttendance).all()

# endpoint to view teacher's attendance using record_id
@router.get("/teacher/{record_id}", response_model=TeacherAttendanceResponse)
def get_teacher_attendance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(TeacherAttendance.record_id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Teacher attendance not found")
    return record

# endpoint to view summary of a teacher's attendance using filters
@router.get("/summary/{teacher_id}", response_model=TeacherAttendanceSummary)
def teacher_summary(teacher_id: int, date_from: date, date_to: date, db: Session = Depends(get_db)):
    q = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == teacher_id,
        TeacherAttendance.date.between(date_from, date_to)
    )

    total = q.count()
    present = q.filter(TeacherAttendance.status == "P").count()
    absent = q.filter(TeacherAttendance.status == "A").count()
    leave = q.filter(TeacherAttendance.status == "L").count()

    percentage = round((present / total) * 100, 2) if total else 0.0

    return TeacherAttendanceSummary(
        teacher_id=teacher_id,
        total_days=total,
        present=present,
        absent=absent,
        leave=leave,
        percentage=percentage
    )

# endpoint to update attendance of any teacher
@router.put("/teacher/{record_id}", response_model=TeacherAttendanceResponse)
def update_teacher_attendance(record_id: int, payload: TeacherAttendanceCreate, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(TeacherAttendance.record_id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Teacher attendance not found")

    for key, value in payload.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

# endpoint to delete attendance record of any teacher using record_id
@router.delete("/teacher/{record_id}")
def delete_teacher_attendance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(TeacherAttendance.record_id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Teacher attendance not found")

    db.delete(record)
    db.commit()
    return {"message": "Teacher attendance deleted"}
