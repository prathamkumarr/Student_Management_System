from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, date
from typing import List

from Backends.Shared.connection import get_db
from Backends.Shared.schemas.attendance_schemas import (
    MarkAttendanceBulk, MarkAttendanceItem, AttendanceFilter,
    UpdateAttendanceItem, AttendanceOut,
    StudentAttendanceResponse, AttendanceSummary,
    TeacherAttendanceCreate, TeacherAttendanceSummary,
    TeacherAttendanceResponse,
)
from Backends.Shared.models.teacher_attendance_models import TeacherAttendance
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.attendance_models import AttendanceRecord

router = APIRouter(prefix="/teacher/attendance", tags=["Teacher Attendance Management"])

# ----STUDENT ATTENDANCE----
# endpoint for marking attendance indiviually
@router.post("/student/mark", status_code=201)
def mark_attendance(attendance: MarkAttendanceItem, db: Session = Depends(get_db)):
    # Checking student existence
    student = db.execute(
        text("SELECT full_name FROM students_master WHERE student_id = :sid"),
        {"sid": attendance.student_id}
    ).fetchone()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student ID {attendance.student_id} not found")

    # Checking subject existence
    subject = db.execute(
        text("SELECT subject_name FROM subjects_master WHERE subject_id = :subid"),
        {"subid": attendance.subject_id}
    ).fetchone()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject ID {attendance.subject_id} not found")

    # Checking for existing of attendance
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == attendance.student_id,
        AttendanceRecord.subject_id == attendance.subject_id,
        AttendanceRecord.class_id == attendance.class_id,
        AttendanceRecord.lecture_date == attendance.lecture_date
    ).one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Attendance already marked for student {attendance.student_id} on {attendance.lecture_date}"
        )

    # Inserting new record with actual names fetched from DB
    new_record = AttendanceRecord(
        student_id=attendance.student_id,
        subject_id=attendance.subject_id,
        class_id=attendance.class_id,
        lecture_date=attendance.lecture_date,
        status=attendance.status,
        remarks=attendance.remarks,
        student_name=student[0],
        subject_name=subject[0]
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "id": new_record.attendance_id,
        "student_id": new_record.student_id,
        "student_name": new_record.student_name,
        "subject_id": new_record.subject_id,
        "subject_name": new_record.subject_name,
        "date": new_record.lecture_date,
        "status": new_record.status,
        "remarks": new_record.remarks
    }

# endpoint for marking attendance in bulk 
@router.post("/student/mark-bulk", status_code=201)
def mark_bulk(payload: MarkAttendanceBulk, db: Session = Depends(get_db)):

    # Parse absent IDs safely
    try:
        absentees = [
            int(x.strip()) for x in payload.absent_ids.split(",") if x.strip()
        ]
    except:
        raise HTTPException(
            status_code=400,
            detail="Absent IDs must be comma-separated numbers"
        )

    class_id = payload.class_id
    subject_id = payload.subject_id
    lecture_date = payload.lecture_date

    # Fetch subject name
    subject_row = db.execute(
        text("SELECT subject_name FROM subjects_master WHERE subject_id = :sid"),
        {"sid": subject_id}
    ).fetchone()

    if not subject_row:
        raise HTTPException(status_code=404, detail="Subject not found")

    subject_name = subject_row[0]

    # Fetch all students of this class 
    student_data = db.execute(
        text("SELECT student_id, full_name FROM students_master WHERE class_id = :cid"),
        {"cid": class_id}
    ).fetchall()

    if not student_data:
        raise HTTPException(status_code=404, detail="No students found for this class")

    processed = 0

    for sid, student_name in student_data:
        status = "A" if sid in absentees else "P"
        remarks = "Absent" if sid in absentees else "Present"

        existing = db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == sid,
            AttendanceRecord.class_id == class_id,
            AttendanceRecord.subject_id == subject_id,
            AttendanceRecord.lecture_date == lecture_date
        ).one_or_none()

        if existing:
            existing.status = status
            existing.remarks = remarks
            existing.subject_name = subject_name
            existing.student_name = student_name

        else:
            db.add(AttendanceRecord(
                student_id=sid,
                student_name=student_name,
                subject_id=subject_id,
                subject_name=subject_name,
                class_id=class_id,
                lecture_date=lecture_date,
                status=status,
                remarks=remarks
            ))

        processed += 1

    db.commit()

    return {"message": f"{processed} attendance records processed"}


# endpoint to view attendance of a student using attendance_id
@router.get("/student/{attendance_id}", response_model=StudentAttendanceResponse)
def get_student_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance record not found")
    return record


# endpoint to update any students attendance using attendance_id 
@router.put("/student/update/{attendance_id}", response_model=StudentAttendanceResponse)
def update_student_attendance(attendance_id: int, payload: UpdateAttendanceItem, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance not found")

    for key, value in payload.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


# endpoint to delete any attendance of a student
@router.delete("/student/delete/{attendance_id}", status_code=204)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    rec = db.query(AttendanceRecord).get(attendance_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(rec)
    db.commit()
    return {"message": "Attendance record deleted successfully"}

# ----TEACHER's OWN ATTENDANCE----
# endpoint for teacher to mark self attendance
@router.post("/mark-self", response_model=TeacherAttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_teacher_attendance(payload: TeacherAttendanceCreate, db: Session = Depends(get_db)):
    # Verify teacher
    teacher = db.query(TeacherMaster).filter_by(teacher_id=payload.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail=f"Teacher ID {payload.teacher_id} not found")

    # Prevent duplicate entry
    existing = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == payload.teacher_id,
        TeacherAttendance.date == payload.date
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")

    new_attendance = TeacherAttendance(
        teacher_id=payload.teacher_id,
        date=payload.date,
        check_in=payload.check_in or datetime.now(),
        status=payload.status,
        remarks=payload.remarks
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


# ----FETCH ATTENDANCE RECORDS----
# endpoint to view student's attendance records(all)
@router.get("/students/attendance", response_model=list[StudentAttendanceResponse])
def get_all_student_attendance(db: Session = Depends(get_db)):
    records = db.query(AttendanceRecord).all()
    return records

# endpoint to view student's attendance records(using date filters)
@router.post("/student/by-date", response_model=List[AttendanceOut])
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

# ----SELF RECORDS----
# ----SELF FILTERED ATTENDANCE (DATE RANGE)----
@router.get("/self/{teacher_id}", response_model=list[TeacherAttendanceResponse])
def get_teacher_attendance_filtered(
    teacher_id: int,
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db)
    ):
    records = (
        db.query(TeacherAttendance)
        .filter(
            TeacherAttendance.teacher_id == teacher_id,
            TeacherAttendance.date.between(date_from, date_to)
        )
        .order_by(TeacherAttendance.date.asc())
        .all()
    )
    return records

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
