from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, date
from typing import List

from Backends.Shared.connection import get_db
from Backends.Backend_admin.schemas.attendance_schemas import (
    MarkAttendanceBulk, MarkAttendanceItem, AttendanceFilter,
    UpdateAttendanceItem, AttendanceOut,
    StudentAttendanceResponse, AttendanceSummary,
    TeacherAttendanceCreate, TeacherAttendanceSummary,
    TeacherAttendanceResponse,
)
from Backends.Backend_teachers.models.attendance_models import (
    AttendanceRecord,
    TeacherAttendance,
)
from Backends.Shared.models.teachers_master import TeacherMaster

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
    if not payload.items:
        raise HTTPException(status_code=400, detail="No attendance records provided")

    # Extract base info from first item
    first_item = payload.items[0]
    class_id = first_item.class_id
    subject_id = first_item.subject_id
    lecture_date = first_item.lecture_date

    # Get subject name from master table
    subject_row = db.execute(
        text("SELECT subject_name FROM subjects_master WHERE subject_id = :subid"),
        {"subid": subject_id}
    ).fetchone()
    if not subject_row:
        raise HTTPException(status_code=404, detail=f"Subject ID {subject_id} not found")

    subject_name = subject_row[0]

    # Get all students in this class (id + name)
    student_data = db.execute(
        text("SELECT student_id, full_name FROM students_master WHERE class_id = :cid"),
        {"cid": class_id}
    ).fetchall()

    if not student_data:
        raise HTTPException(status_code=404, detail=f"No students found for class ID {class_id}")

    absentees = [item.student_id for item in payload.items]
    processed = 0

    for sid, student_name in student_data:
        status = "A" if sid in absentees else "P"
        remarks = "Absent" if sid in absentees else "Present"

        # Check if record already exists (same class, subject, student, and date)
        existing = db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == sid,
            AttendanceRecord.subject_id == subject_id,
            AttendanceRecord.class_id == class_id,
            AttendanceRecord.lecture_date == lecture_date
        ).one_or_none()

        if existing:
            # Update only if something actually changed
            if existing.status != status or existing.remarks != remarks:
                existing.status = status
                existing.remarks = remarks
                existing.subject_name = subject_name
                existing.student_name = student_name
        else:
            # Create new attendance record
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

    return {"message": f"{processed} attendance records processed successfully"}

# endpoint to update attendance of a student
@router.put("/student/update", status_code=200)
def update_attendance(item: UpdateAttendanceItem, db: Session = Depends(get_db)):
    # Find existing record
    record = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == item.student_id,
        AttendanceRecord.subject_id == item.subject_id,
        AttendanceRecord.class_id == item.class_id,
        AttendanceRecord.lecture_date == item.lecture_date
    ).one_or_none()

    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"No attendance found for student {item.student_id} on {item.lecture_date}"
        )

    # Update allowed fields only
    record.status = item.status
    record.remarks = item.remarks
    record.updated_at = datetime.now() 

    db.commit()
    db.refresh(record)

    return {
        "message": "Attendance record updated successfully",
        "attendance_id": record.attendance_id,
        "student_id": record.student_id,
        "subject_id": record.subject_id,
        "class_id": record.class_id,
        "lecture_date": record.lecture_date,
        "status": record.status,
        "remarks": record.remarks,
        "updated_at": record.updated_at
    }

# endpoint to delete any attendance of a student
@router.delete("/student/{attendance_id}", status_code=204)
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

# ----SELF RECORDS----
# endpoint to view all teacher's self attendance records
@router.get("/teachers", response_model=list[TeacherAttendanceResponse])
def get_all_teacher_attendance(db: Session = Depends(get_db)):
    records = db.query(TeacherAttendance).all()
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
