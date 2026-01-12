from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from datetime import datetime, timezone

from Backends.Shared.models.employee_salary_models import EmployeeSalary
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.staff_separation_models import StaffSeparation
from Backends.Shared.schemas.staff_separation_schemas import (
    StaffSeparationCreate, StaffSeparationResponse, RejectRequest
)
from Backends.Shared.models.credentials_models import StaffCredential
from Backends.Shared.enums.separation_enums import SeparationStatus
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/admin/staff/separation",
    tags=["staff Separation"],
    dependencies=[Depends(get_current_session)]
)

# endpoint to issue separation
@router.post("/issue", response_model=StaffSeparationResponse)
def issue_separation(payload: StaffSeparationCreate, db: Session = Depends(get_db)):

    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == payload.staff_id,
        StaffMaster.is_active == True
    ).first()

    if not staff:
        raise HTTPException(404, "Active staff not found")

    # only one pending separation allowed
    existing = db.query(StaffSeparation).filter(
        StaffSeparation.teacher_id == payload.staff_id,
        StaffSeparation.status == SeparationStatus.PENDING
    ).first()

    if existing:
        raise HTTPException(400, "Pending separation already exists")

    sep = StaffSeparation(
        staff_id=payload.staff_id,
        reason=payload.reason,
        remarks=payload.remarks,
        separation_date=payload.separation_date,
        status=SeparationStatus.PENDING
    )

    db.add(sep)
    db.commit()
    db.refresh(sep)

    return sep


# endpoint to view all separation requests
@router.get("/all", response_model=list[StaffSeparationResponse])
def get_all_separations(status: SeparationStatus | None = None, db: Session = Depends(get_db)):
    q = db.query(StaffSeparation)
    if status:
        q = q.filter(StaffSeparation.status == status)
    return q.all()

# endpoint to view separation by ID
@router.get("/{sep_id}", response_model=StaffSeparationResponse)
def get_separation(sep_id: int, db: Session = Depends(get_db)):
    entry = db.query(StaffSeparation).filter(
        StaffSeparation.sep_id == sep_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Separation record not found")

    return entry

# endpoint to approve separation
@router.post("/approve/{sep_id}")
def approve_separation(
    sep_id: int, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

    sep = (
        db.query(StaffSeparation)
        .filter(
            StaffSeparation.sep_id == sep_id,
            StaffSeparation.status == SeparationStatus.PENDING
        )
        .with_for_update()
        .first()
    )

    if not sep:
        raise HTTPException(404, "Pending separation not found")

    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == sep.staff_id,
        StaffMaster.is_active == True
    ).first()

    if not staff:
        raise HTTPException(400, "Staff already inactive")

    try:
        # deactivate staff
        staff.is_active = False

        # deactivate salary
        db.query(EmployeeSalary).filter(
            EmployeeSalary.employee_type == "staff",
            EmployeeSalary.employee_id == sep.staff_id,
            EmployeeSalary.is_active == True
        ).update({"is_active": False})

        # deactivate credentials
        db.query(StaffCredential).filter(
            StaffCredential.staff_id == sep.staff_id,
            StaffCredential.is_active == True
        ).update({"is_active": False})

        # update separation
        sep.status = SeparationStatus.APPROVED
        sep.approved_at = datetime.now(timezone.utc)
        sep.academic_session_id = session.session_id

        db.commit()

        return {
            "message": "Staff separation approved",
            "staff_id": sep.staff_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
    

# endpoint to reject a request
@router.post("/reject/{sep_id}")
def reject_separation(sep_id: int, payload: RejectRequest, db: Session = Depends(get_db)):

    sep = db.query(StaffSeparation).filter(
        StaffSeparation.sep_id == sep_id,
        StaffSeparation.status == SeparationStatus.PENDING
    ).first()

    if not sep:
        raise HTTPException(404, "Pending separation not found")

    sep.status = SeparationStatus.REJECTED
    sep.remarks = payload.reason
    sep.rejected_at = datetime.now(timezone.utc)

    db.commit()

    return {"message": "Separation rejected"}