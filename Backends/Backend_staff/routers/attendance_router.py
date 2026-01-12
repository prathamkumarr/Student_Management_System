from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, date, timezone

from Backends.Shared.connection import get_db
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.staff_attendance_models import StaffAttendance
from Backends.Shared.schemas.attendance_schemas import (
    StaffAttendanceCreate, StaffAttendanceResponse
    )
from Backends.Shared.enums.attendance_enums import AttendanceStatus
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/staff/attendance", tags=["Staff Attendance Management"],
    dependencies=[Depends(get_current_session)]
    )

# =====================================================
# STAFF SELF ATTENDANCE
# =====================================================

@router.post("/mark-self", response_model=StaffAttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_staff_attendance(
    payload: StaffAttendanceCreate, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == payload.staff_id
    ).first()

    if not staff:
        raise HTTPException(404, "Staff not found")

    if not staff.is_active:
        raise HTTPException(
            status_code=400,
            detail="Attendance cannot be marked — staff is inactive"
        )
    existing = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == payload.staff_id,
        StaffAttendance.date == payload.date
    ).first()

    if existing:
        raise HTTPException(
        status_code=400,
        detail="Attendance already marked for today"
    )

    record = StaffAttendance(
        staff_id=payload.staff_id,
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


@router.put("/check-out/{record_id}", response_model=StaffAttendanceResponse)
def staff_check_out(record_id: int, db: Session = Depends(get_db)):
    record = db.query(StaffAttendance).filter(
        StaffAttendance.record_id == record_id,
        StaffAttendance.is_active == True
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
@router.get("/today/{staff_id}")
def get_today_attendance(staff_id: int, db: Session = Depends(get_db)):
    today = date.today()

    record = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == staff_id,
        StaffAttendance.date == today,
        StaffAttendance.is_active == True
    ).first()

    if not record:
        raise HTTPException(404, "Attendance not marked")

    return {
        "record_id": record.record_id,
        "status": record.status,
        "check_out": record.check_out
    }

# =====================================================
# SELF REPORTS
# =====================================================
@router.get("/self/{staff_id}")
def get_staff_attendance_range(
    staff_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db)
):
    # ---- validate staff ----
    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == staff_id
    ).first()

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    if date_from > date_to:
        raise HTTPException(
            status_code=400,
            detail="date_from cannot be after date_to"
        )

    records = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == staff_id,
        StaffAttendance.date >= date_from,
        StaffAttendance.date <= date_to,
        StaffAttendance.is_active == True
    ).order_by(StaffAttendance.date.asc()).all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No attendance records found for given date range"
        )

    return records


@router.get("/summary/{staff_id}")
def get_staff_attendance_summary(
    staff_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db)
):
    # ---- validate staff ----
    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == staff_id
    ).first()

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    if date_from > date_to:
        raise HTTPException(
            status_code=400,
            detail="date_from cannot be after date_to"
        )

    # ---- base query ----
    records = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == staff_id,
        StaffAttendance.date >= date_from,
        StaffAttendance.date <= date_to,
        StaffAttendance.is_active == True
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
        "staff_id": staff_id,
        "date_from": date_from,
        "date_to": date_to,
        "total_days": total_days,
        "present_days": present,
        "absent_days": absent,
        "late_days": late,
        "leave_days": leave
    }