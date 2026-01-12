from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, date, timezone
from typing import List
from sqlalchemy.exc import IntegrityError

from Backends.Shared.connection import get_db
from Backends.Shared.schemas.attendance_schemas import (
    MarkAttendanceBulk,
    MarkAttendanceItem,
    AttendanceFilter,
    UpdateAttendanceItem,
    AttendanceOut,
    StudentAttendanceResponse,
    AttendanceSummary,
    TeacherAttendanceCreate,
    TeacherAttendanceResponse,
)
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.subjects_master import SubjectMaster
from Backends.Shared.models.teacher_attendance_models import TeacherAttendance
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.attendance_models import AttendanceRecord
from Backends.Shared.enums.attendance_enums import AttendanceStatus
from Backends.Shared.models.class_subjects_model import ClassSubject
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/teacher/attendance",
    tags=["Teacher Attendance Management"],
    dependencies=[Depends(get_current_session)]
)

# =====================================================
# STUDENT ATTENDANCE
# =====================================================

@router.post("/student/mark", status_code=201)
def mark_attendance(
    payload: MarkAttendanceItem, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == payload.student_id
        ).first()

    if not student:
        raise HTTPException(404, "Student not found")

    if not student.is_active:
        raise HTTPException(
        status_code=400,
        detail="Attendance cannot be marked — student is inactive"
        )

    subject = db.query(SubjectMaster).filter(
        SubjectMaster.subject_id == payload.subject_id
        ).first()

    if not subject:
        raise HTTPException(404, "Subject not found")
    
    exists = db.query(ClassSubject).filter(
        ClassSubject.class_id == student.class_id,
        ClassSubject.subject_id == payload.subject_id,
        ClassSubject.is_active == True
    ).first()

    if not exists:
        raise HTTPException(
        status_code=400,
        detail="Subject not assigned to student's class"
        )
    student = db.get(StudentMaster, payload.student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == payload.student_id,
        AttendanceRecord.subject_id == payload.subject_id,
        AttendanceRecord.class_id == student.class_id,
        AttendanceRecord.lecture_date == payload.lecture_date
    ).one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this lecture"
        )

    record = AttendanceRecord(
        student_id=payload.student_id,
        subject_id=payload.subject_id,
        class_id=student.class_id,
        teacher_id=payload.teacher_id,
        lecture_date=payload.lecture_date,
        status=AttendanceStatus(payload.status),
        remarks=payload.remarks,
        academic_session_id=session.session_id
    )

    db.add(record)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
        status_code=400,
        detail="Attendance already marked for this lecture")

    db.refresh(record)

    return record


# -----------------------------------------------------

@router.post("/student/mark-bulk", status_code=201)
def mark_bulk(
    payload: MarkAttendanceBulk, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

    absentees = payload.absent_ids

    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == payload.class_id
        ).all()

    if not students:
        raise HTTPException(404, "No students found for this class")
    
    subject = db.query(SubjectMaster).filter(
        SubjectMaster.subject_id == payload.subject_id
        ).first()

    if not subject:
        raise HTTPException(404, "Subject not found")
    
    exists = db.query(ClassSubject).filter(
        ClassSubject.class_id == payload.class_id,
        ClassSubject.subject_id == payload.subject_id,
        ClassSubject.is_active == True
    ).first()

    if not exists:
        raise HTTPException(
        status_code=400,
        detail="Subject not assigned to student's class"
        )
    
    processed = 0

    for student in students:
        if not student.is_active:
            continue

        student_id = student.student_id

        status = (AttendanceStatus.A if student_id in absentees else AttendanceStatus.P)

        remarks = ("Absent" if status == AttendanceStatus.A else "Present")

        record = db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.subject_id == payload.subject_id,
            AttendanceRecord.class_id == payload.class_id,
            AttendanceRecord.lecture_date == payload.lecture_date
        ).one_or_none()

        if record:
            record.status = status
            record.remarks = remarks
        else:
            db.add(AttendanceRecord(
                student_id=student_id,
                subject_id=payload.subject_id,
                class_id=payload.class_id,
                teacher_id=payload.teacher_id,
                lecture_date=payload.lecture_date,
                status=status,
                academic_session_id=session.session_id,
                remarks=remarks
            ))

        processed += 1

    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
        status_code=400,
        detail="Some attendance records were already marked"
        )
    return {"message": f"{processed} attendance records processed"}


# =====================================================
# VIEW / UPDATE / DELETE
# =====================================================

@router.get("/student/{attendance_id}", response_model=StudentAttendanceResponse)
def get_student_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceRecord).filter(
        AttendanceRecord.attendance_id == attendance_id
    ).first()

    if not record:
        raise HTTPException(404, "Attendance record not found")

    return record


@router.put("/student/update/{attendance_id}", response_model=StudentAttendanceResponse)
def update_student_attendance(
    attendance_id: int,
    payload: UpdateAttendanceItem,
    db: Session = Depends(get_db)
):
    record = db.query(AttendanceRecord).filter(
        AttendanceRecord.attendance_id == attendance_id
    ).first()

    if not record:
        raise HTTPException(404, "Attendance record not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

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


# =====================================================
# TEACHER SELF ATTENDANCE
# =====================================================

@router.post("/mark-self", response_model=TeacherAttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_teacher_attendance(
    payload: TeacherAttendanceCreate, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == payload.teacher_id
    ).first()

    if not teacher:
        raise HTTPException(404, "Teacher not found")

    if not teacher.is_active:
        raise HTTPException(
            status_code=400,
            detail="Attendance cannot be marked — teacher is inactive"
        )
    existing = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == payload.teacher_id,
        TeacherAttendance.date == payload.date
    ).first()

    if existing:
        raise HTTPException(
        status_code=400,
        detail="Attendance already marked for today"
    )

    record = TeacherAttendance(
        teacher_id=payload.teacher_id,
        date=payload.date,
        check_in = datetime.now(timezone.utc),
        status=payload.status,
        academic_session_id=session.session_id,
        remarks=payload.remarks
    )

    db.add(record)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked"
        )

    db.refresh(record)
    return record


@router.put("/check-out/{record_id}", response_model=TeacherAttendanceResponse)
def teacher_check_out(record_id: int, db: Session = Depends(get_db)):
    record = db.query(TeacherAttendance).filter(
        TeacherAttendance.record_id == record_id,
        TeacherAttendance.is_active == True
    ).first()

    if not record:
        raise HTTPException(404, "Attendance record not found")

    if record.check_out:
        raise HTTPException(400, "Already checked out")

    record.check_out = datetime.now()

    if (
        record.status == AttendanceStatus.P
        and record.check_out.date() > record.date
    ):
        record.status = AttendanceStatus.L   # Late

    db.commit()
    db.refresh(record)
    return record


# ----------------------------------------------------
@router.get("/today/{teacher_id}")
def get_today_attendance(teacher_id: int, db: Session = Depends(get_db)):
    today = date.today()

    record = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == teacher_id,
        TeacherAttendance.date == today,
        TeacherAttendance.is_active == True
    ).first()

    if not record:
        raise HTTPException(404, "Attendance not marked")

    return {
        "record_id": record.record_id,
        "status": record.status,
        "check_out": record.check_out
    }


# =====================================================
# REPORTS
# =====================================================

@router.post("/student/by-date", response_model=List[AttendanceOut])
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


@router.get("/student/summary/{student_id}", response_model=AttendanceSummary)
def summary(
    student_id: int,
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db)
):
    q = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.lecture_date.between(date_from, date_to)
    )

    total = q.count()
    present = q.filter(AttendanceRecord.status == "P").count()
    absent = q.filter(AttendanceRecord.status == "A").count()
    late = q.filter(AttendanceRecord.status == "L").count()
    leave = q.filter(AttendanceRecord.status == "LE").count()

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


# =====================================================
# SELF REPORTS
# =====================================================
@router.get("/self/{teacher_id}")
def get_teacher_attendance_range(
    teacher_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db)
):
    # ---- validate teacher ----
    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == teacher_id
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    if date_from > date_to:
        raise HTTPException(
            status_code=400,
            detail="date_from cannot be after date_to"
        )

    records = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == teacher_id,
        TeacherAttendance.date >= date_from,
        TeacherAttendance.date <= date_to,
        TeacherAttendance.is_active == True
    ).order_by(TeacherAttendance.date.asc()).all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No attendance records found for given date range"
        )

    return records


@router.get("/summary/{teacher_id}")
def get_teacher_attendance_summary(
    teacher_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db)
):
    # ---- validate teacher ----
    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == teacher_id
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    if date_from > date_to:
        raise HTTPException(
            status_code=400,
            detail="date_from cannot be after date_to"
        )

    # ---- base query ----
    records = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_id == teacher_id,
        TeacherAttendance.date >= date_from,
        TeacherAttendance.date <= date_to,
        TeacherAttendance.is_active == True
    ).all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No attendance records found for given date range"
        )

    # ---- summary counts ----
    total_days = len(records)
    present = sum(1 for r in records if r.status == AttendanceStatus.P)
    absent = sum(1 for r in records if r.status == AttendanceStatus.A)
    late = sum(1 for r in records if r.status == AttendanceStatus.L)
    leave = sum(1 for r in records if r.status == AttendanceStatus.LE)

    return {
        "teacher_id": teacher_id,
        "date_from": date_from,
        "date_to": date_to,
        "total_days": total_days,
        "present_days": present,
        "absent_days": absent,
        "late_days": late,
        "leave_days": leave
    }