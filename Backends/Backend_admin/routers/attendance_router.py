from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from datetime import date
from typing import List
# Schemas
from Backends.Shared.schemas.attendance_schemas import (
    AttendanceSummary, AttendanceOut, StudentAttendanceResponse,
    AttendanceFilter, UpdateAttendanceItem,
    TeacherAttendanceUpdate, TeacherAttendanceSummary,
    TeacherAttendanceResponse, StaffAttendanceResponse,
    StaffAttendanceSummary, StaffAttendanceUpdate
)
from Backends.Shared.enums.attendance_enums import AttendanceStatus

# Models
from Backends.Shared.models.teacher_attendance_models import TeacherAttendance
from Backends.Shared.models.attendance_models import AttendanceRecord
from Backends.Shared.models.staff_attendance_models import StaffAttendance

router = APIRouter(prefix="/admin/attendance", tags=["Admin Attendance"])

# -----STUDENT ATTENDANCE-----
# endpoint to view all student's attendance 
@router.get("/student", response_model=list[StudentAttendanceResponse])
def get_all_student_attendance(db: Session = Depends(get_db)):
    return db.query(AttendanceRecord).filter(
                    AttendanceRecord.is_active == True
                    ).all()

# endpoint to view attendance of a student using attendance_id
@router.get("/student/{attendance_id}", response_model=StudentAttendanceResponse)
def get_student_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(
        AttendanceRecord.attendance_id == attendance_id,
        AttendanceRecord.is_active == True
        ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance record not found")
    return record

# endpoint to view student's attendance records(using date filters)
@router.post("/student/by-date", response_model=List[AttendanceOut])
def get_by_student(filter: AttendanceFilter, db: Session = Depends(get_db)):

    # Clean filters
    student_id = filter.student_id
    subject_id = filter.subject_id
    date_from = filter.date_from
    date_to = filter.date_to

    # Base Query
    q = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.lecture_date >= date_from,
        AttendanceRecord.lecture_date <= date_to,
        AttendanceRecord.is_active == True
    )

    # Subject filtering ONLY if valid
    if subject_id and subject_id > 0:
        q = q.filter(AttendanceRecord.subject_id == subject_id)

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
        AttendanceRecord.lecture_date.between(date_from, date_to),
        AttendanceRecord.is_active == True
    )
    total = q.count()
    present = q.filter(AttendanceRecord.status == AttendanceStatus.P).count()
    absent = q.filter(AttendanceRecord.status == AttendanceStatus.A).count()
    late = q.filter(AttendanceRecord.status == AttendanceStatus.L).count()
    leave = q.filter(AttendanceRecord.status == AttendanceStatus.LE).count()

    percentage = round((present / total) * 100, 2) if total else 0.0

    return AttendanceSummary(
        student_id=student_id,
        total_lectures=total,
        present=present,
        absent=absent,
        late=late,
        leave=leave,
        percentage=percentage
    )

# endpoint to update any students attendance using attendance_id 
@router.put("/student/update/{attendance_id}", response_model=StudentAttendanceResponse)
def update_student_attendance(attendance_id: int, payload: UpdateAttendanceItem, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id,
                                               AttendanceRecord.is_active == True
                                            ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance not found")

    record.status = payload.status
    record.remarks = payload.remarks

    db.commit()
    db.refresh(record)
    return record

# endpoint to delete attendance of any student using attendance_id
@router.delete("/student/delete/{attendance_id}")
def delete_student_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == attendance_id,
                                               AttendanceRecord.is_active == True
                                            ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Student attendance not found")

    record.is_active = False

    db.commit()
    return {"message": "Student attendance deleted"}


# -----TEACHER ATTENDANCE----- 
# endpoint to view teachers attendance
@router.get("/teacher", response_model=list[TeacherAttendanceResponse])
def get_all_teacher_attendance(db: Session = Depends(get_db)):
    return(
        db.query(TeacherAttendance).filter(
        TeacherAttendance.is_active == True).all()
    )

# endpoint to view teacher's attendance using record_id
@router.get("/teacher/{record_id}", response_model=TeacherAttendanceResponse)
def get_teacher_attendance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(TeacherAttendance.record_id == record_id,
                                                TeacherAttendance.is_active == True
                                                ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Teacher attendance not found")
    return record

# endpoint to view summary of a teacher's attendance using filters
@router.get("/teacher/summary/{teacher_id}", response_model=TeacherAttendanceSummary)
def teacher_summary(teacher_id: int, date_from: date, date_to: date, db: Session = Depends(get_db)):
    q = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == teacher_id,
        TeacherAttendance.date.between(date_from, date_to),
        TeacherAttendance.is_active == True
    )

    total = q.count()
    present = q.filter(TeacherAttendance.status == AttendanceStatus.P).count()
    absent = q.filter(TeacherAttendance.status == AttendanceStatus.A).count()
    leave = q.filter(TeacherAttendance.status == AttendanceStatus.LE).count()

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
@router.put("/teacher/update/{record_id}", response_model=TeacherAttendanceResponse)
def update_teacher_attendance(record_id: int, payload: TeacherAttendanceUpdate, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(TeacherAttendance.record_id == record_id,
                                                TeacherAttendance.is_active == True
                                                ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Teacher attendance not found")

    if payload.check_out is not None:
        record.check_out = payload.check_out
    if payload.status is not None:
        record.status = payload.status
    if payload.remarks is not None:
        record.remarks = payload.remarks

    db.commit()
    db.refresh(record)
    return record

# endpoint to delete attendance record of any teacher using record_id
@router.delete("/teacher/delete/{record_id}")
def delete_teacher_attendance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(TeacherAttendance.record_id == record_id,
                                                TeacherAttendance.is_active == True
                                                ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Teacher attendance not found")

    record.is_active = False
    db.commit()

    return {"message": "Teacher attendance deleted"}


# ----- STAFF ATTENDANCE ----- 
# endpoint to view staff's attendance
@router.get("/staff", response_model=list[StaffAttendanceResponse])
def get_all_staff_attendance(db: Session = Depends(get_db)):
    return(
        db.query(StaffAttendance).filter(
        StaffAttendance.is_active == True).all()
    )

# endpoint to view staff's attendance using record_id
@router.get("/staff/{record_id}", response_model=StaffAttendanceResponse)
def get_staff_attendance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(StaffAttendance).filter(StaffAttendance.record_id == record_id,
                                              StaffAttendance.is_active == True
                                            ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Staff attendance not found")
    return record

# endpoint to view summary of a staff's attendance using filters
@router.get("/staff/summary/{staff_id}", response_model=StaffAttendanceSummary)
def staff_summary(staff_id: int, date_from: date, date_to: date, db: Session = Depends(get_db)):
    q = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == staff_id,
        StaffAttendance.date.between(date_from, date_to),
        StaffAttendance.is_active == True
    )

    total = q.count()
    present = q.filter(StaffAttendance.status == AttendanceStatus.P).count()
    absent = q.filter(StaffAttendance.status == AttendanceStatus.A).count()
    leave = q.filter(StaffAttendance.status == AttendanceStatus.LE).count()

    percentage = round((present / total) * 100, 2) if total else 0.0

    return StaffAttendanceSummary(
        staff_id=staff_id,
        total_days=total,
        present=present,
        absent=absent,
        leave=leave,
        percentage=percentage
    )

# endpoint to update attendance of any staff member
@router.put("/staff/update/{record_id}", response_model=StaffAttendanceResponse)
def update_staff_attendance(record_id: int, payload: StaffAttendanceUpdate, db: Session = Depends(get_db)):
    record = db.query(StaffAttendance).filter(StaffAttendance.record_id == record_id,
                                              StaffAttendance.is_active == True
                                            ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Staff member attendance not found")

    if payload.check_out is not None:
        record.check_out = payload.check_out
    if payload.status is not None:
        record.status = payload.status
    if payload.remarks is not None:
        record.remarks = payload.remarks

    db.commit()
    db.refresh(record)
    return record

# endpoint to delete attendance record of any staff member using record_id
@router.delete("/staff/delete/{record_id}")
def delete_staff_attendance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(StaffAttendance).filter(StaffAttendance.record_id == record_id,
                                              StaffAttendance.is_active == True
                                            ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Staff member attendance not found")

    record.is_active = False
    db.commit()
    return {"message": "Staff's attendance deleted"}