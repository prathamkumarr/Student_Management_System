from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date

from Backends.Shared.connection import get_db
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.staff_attendance_models import StaffAttendance
from Backends.Shared.schemas.attendance_schemas import (
    StaffAttendanceCreate, StaffAttendanceResponse, StaffAttendanceSummary
    )

router = APIRouter(prefix="/staff/attendance", tags=["Staff Attendance Management"])

# ----STAFF MEMBER's OWN ATTENDANCE----
# endpoint for staff to mark self attendance
@router.post("/mark-self", response_model=StaffAttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_staff_attendance(payload: StaffAttendanceCreate, db: Session = Depends(get_db)):
    # Verify staff member
    staff = db.query(StaffMaster).filter_by(staff_id=payload.staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail=f"Staff ID {payload.staff_id} not found")

    # Prevent duplicate entry
    existing = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == payload.staff_id,
        StaffAttendance.date == payload.date
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")

    new_attendance = StaffAttendance(
        staff_id=payload.staff_id,
        date=payload.date,
        check_in=payload.check_in or datetime.now(),
        status=payload.status,
        remarks=payload.remarks
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


# ----SELF RECORDS----
# ----SELF FILTERED ATTENDANCE (DATE RANGE)----
@router.get("/self/{staff_id}", response_model=list[StaffAttendanceResponse])
def get_staff_attendance_filtered(
    staff_id: int,
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db)
    ):
    records = (
        db.query(StaffAttendance)
        .filter(
            StaffAttendance.staff_id == staff_id,
            StaffAttendance.date.between(date_from, date_to)
        )
        .order_by(StaffAttendance.date.asc())
        .all()
    )
    return records

# endpoint to view summary of a staff member's attendance using filters
@router.get("/summary/{staff_id}", response_model=StaffAttendanceSummary)
def staff_summary(staff_id: int, date_from: date, date_to: date, db: Session = Depends(get_db)):
    q = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == staff_id,
        StaffAttendance.date.between(date_from, date_to)
    )

    total = q.count()
    present = q.filter(StaffAttendance.status == "P").count()
    absent = q.filter(StaffAttendance.status == "A").count()
    leave = q.filter(StaffAttendance.status == "L").count()

    percentage = round((present / total) * 100, 2) if total else 0.0

    return StaffAttendanceSummary(
        staff_id=staff_id,
        total_days=total,
        present=present,
        absent=absent,
        leave=leave,
        percentage=percentage
    )
