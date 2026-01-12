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
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/admin/tc",
    tags=["Transfer Certificate"],
    dependencies=[Depends(get_current_session)]
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
def approve_tc(
    tc_id: int, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

    tc = (
    db.query(TransferCertificate)
    .filter(
        TransferCertificate.tc_id == tc_id,
        TransferCertificate.is_active == False
    )
    .with_for_update()
    .first()
)

    if not tc:
        raise HTTPException(404, "Pending TC not found")

    affected = db.query(StudentMaster).filter(
        StudentMaster.student_id == tc.student_id,
        StudentMaster.is_active == True
    ).update(
        {"is_active": False},
        synchronize_session=False
    )

    if affected == 0:
        raise HTTPException(400, "Student already inactive")

    try:
        # deactivate credentials
        db.query(StudentCredential).filter(
            StudentCredential.student_id == tc.student_id
        ).update({"is_active": False}, synchronize_session=False)

        # deactivate attendance
        db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == tc.student_id
        ).update({"is_active": False}, synchronize_session=False)

        # deactivate pending fees
        db.query(StudentFee).filter(
            StudentFee.student_id == tc.student_id,
            StudentFee.status == StudentFeeStatus.PENDING
        ).update(
            {"status": StudentFeeStatus.DEACTIVATED},
            synchronize_session=False
        )

        # approve TC
        tc.is_active = True
        tc.academic_session_id = session.session_id   
       
        db.commit()
        return {"message": "TC Approved Successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
