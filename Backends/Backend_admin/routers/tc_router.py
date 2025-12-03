from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.attendance_models import AttendanceRecord
from Backends.Shared.models.fees_models import StudentFee
from Backends.Shared.models.tc_models import TransferCertificate
from Backends.Shared.schemas.tc_schemas import TCCreate, TCResponse

router = APIRouter(
    prefix="/admin/tc",
    tags=["Transfer Certificate"]
)

# endpoint to issue TC
@router.post("/issue", response_model=TCResponse)
def issue_tc(payload: TCCreate, db: Session = Depends(get_db)):

    # Validate student exists
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == payload.student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if already has TC issued
    existing_tc = db.query(TransferCertificate).filter(
        TransferCertificate.student_id == payload.student_id
    ).first()

    if existing_tc:
        raise HTTPException(status_code=400, detail="TC already issued for this student")

    # Mark student as inactive
    student.is_active = False
    db.commit()

    # Deactivate attendance records
    db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == payload.student_id
    ).update({"is_active": False})
    db.commit()

    # Deactivate fee pending entries
    db.query(StudentFee).filter(
        StudentFee.student_id == payload.student_id
    ).update({"status": "DEACTIVATED"})
    db.commit()

    # Create TC record
    tc_entry = TransferCertificate(
        student_id=payload.student_id,
        reason=payload.reason,
        remarks=payload.remarks,
        issue_date=payload.issue_date
    )

    db.add(tc_entry)
    db.commit()
    db.refresh(tc_entry)

    return tc_entry

# endpoint to View all issued TCs
@router.get("/all", response_model=list[TCResponse])
def get_all_tc(db: Session = Depends(get_db)):
    entries = db.query(TransferCertificate).all()
    return entries

# endpoint to view TC by ID
@router.get("/{tc_id}", response_model=TCResponse)
def get_tc(tc_id: int, db: Session = Depends(get_db)):
    tc = db.query(TransferCertificate).filter(
        TransferCertificate.tc_id == tc_id
    ).first()

    if not tc:
        raise HTTPException(status_code=404, detail="TC not found")

    return tc

# endpoint to approve TC
@router.post("/approve/{tc_id}")
def approve_tc(tc_id: int, db: Session = Depends(get_db)):

    tc = db.query(TransferCertificate).filter(
        TransferCertificate.tc_id == tc_id
    ).first()

    if not tc:
        raise HTTPException(status_code=404, detail="TC not found")

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == tc.student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")

    # Just deactivate (DO NOT DELETE)
    student.is_active = False   # add this field in model if needed
    db.commit()

    # Remove Fees
    db.query(StudentFee).filter(
        StudentFee.student_id == tc.student_id
    ).delete()
    db.commit()

    # Remove Attendance
    db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == tc.student_id
    ).delete()
    db.commit()

    # Mark TC as approved
    tc.status = True
    db.commit()

    return {
        "message": "TC Approved Successfully!",
        "student_id": tc.student_id
    }

