from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.attendance_models import AttendanceRecord
from Backends.Shared.models.fees_models import StudentFee
from Backends.Shared.models.tc_models import TransferCertificate
from Backends.Shared.schemas.tc_schemas import TCCreate, TCResponse
from Backends.Shared.models.credentials_models import StudentCredential
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus

router = APIRouter(
    prefix="/admin/tc",
    tags=["Transfer Certificate"]
)

# endpoint to issue TC (REQUEST ONLY)
@router.post("/issue", response_model=TCResponse)
def issue_tc(payload: TCCreate, db: Session = Depends(get_db)):

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == payload.student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Active student not found")

    # Already pending or approved TC
    existing_tc = db.query(TransferCertificate).filter(
        TransferCertificate.student_id == payload.student_id
    ).first()

    if existing_tc:
        raise HTTPException(400, "TC request already exists for this student")

    # Pending fee check (valid business rule)
    pending_fee = db.query(StudentFee).filter(
        StudentFee.student_id == payload.student_id,
        StudentFee.status == "PENDING"
    ).first()

    if pending_fee:
        raise HTTPException(400, "Clear pending fees before issuing TC")

    try:
        tc_entry = TransferCertificate(
            student_id=payload.student_id,
            reason=payload.reason,
            remarks=payload.remarks,
            issue_date=payload.issue_date,
            is_active=False   
        )

        db.add(tc_entry)
        db.commit()
        db.refresh(tc_entry)

        return tc_entry

    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to issue TC")


# endpoint to View all issued TCs
@router.get("/all", response_model=list[TCResponse])
def get_all_tc(
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    q = db.query(TransferCertificate)
    if is_active is not None:
        q = q.filter(TransferCertificate.is_active == is_active)
    return q.all()


# endpoint to view TC by ID
@router.get("/{tc_id}", response_model=TCResponse)
def get_tc(tc_id: int, db: Session = Depends(get_db)):
    tc = db.query(TransferCertificate).filter(
        TransferCertificate.tc_id == tc_id
    ).first()

    if not tc:
        raise HTTPException(status_code=404, detail="TC not found")

    return tc

# endpoint to approve TC (FINAL ACTION)
@router.post("/approve/{tc_id}")
def approve_tc(tc_id: int, db: Session = Depends(get_db)):

    tc = db.query(TransferCertificate).filter(
        TransferCertificate.tc_id == tc_id,
        TransferCertificate.is_active == False  # only pending allowed
    ).first()

    if not tc:
        raise HTTPException(404, "Pending TC not found")

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == tc.student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(400, "Student already inactive")

    try:
        # Deactivate student
        student.is_active = False

        # Deactivate credentials
        db.query(StudentCredential).filter(
            StudentCredential.student_id == tc.student_id
        ).update({"is_active": False})

        # Deactivate attendance
        db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == tc.student_id
        ).update({"is_active": False})

        # Deactivate fees
        db.query(StudentFee).filter(
            StudentFee.student_id == tc.student_id,
            StudentFee.status == StudentFeeStatus.PENDING
        ).update(
            {"status": StudentFeeStatus.DEACTIVATED},
            synchronize_session=False
        )

        # Mark TC approved
        tc.is_active = True

        db.commit()

        return {
            "message": "TC Approved Successfully",
            "student_id": tc.student_id
        }

    except Exception:
        db.rollback()
        raise HTTPException(500, "Failed to approve TC")

