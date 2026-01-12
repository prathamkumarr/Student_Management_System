from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from datetime import datetime, timezone

from Backends.Shared.models.employee_salary_models import EmployeeSalary
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.teacher_separation_models import TeacherSeparation
from Backends.Shared.schemas.teacher_separation_schemas import (
    TeacherSeparationCreate, TeacherSeparationResponse, RejectSeparationRequest
)
from Backends.Shared.models.credentials_models import TeacherCredential
from Backends.Shared.enums.separation_enums import SeparationStatus
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/admin/teachers/separation",
    tags=["Teacher Separation"],
    dependencies=[Depends(get_current_session)]
)

# endpoint to issue separation
@router.post("/issue", response_model=TeacherSeparationResponse)
def issue_separation(payload: TeacherSeparationCreate, db: Session = Depends(get_db)):

    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == payload.teacher_id,
        TeacherMaster.is_active == True
    ).first()

    if not teacher:
        raise HTTPException(404, "Active teacher not found")

    # only one pending separation allowed
    existing = db.query(TeacherSeparation).filter(
        TeacherSeparation.teacher_id == payload.teacher_id,
        TeacherSeparation.status == SeparationStatus.PENDING
    ).first()

    if existing:
        raise HTTPException(400, "Pending separation already exists")

    sep = TeacherSeparation(
        teacher_id=payload.teacher_id,
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
@router.get("/all", response_model=list[TeacherSeparationResponse])
def get_all_separations(status: SeparationStatus | None = None, db: Session = Depends(get_db)):
    q = db.query(TeacherSeparation)
    if status:
        q = q.filter(TeacherSeparation.status == status)
    return q.all()


# endpoint to view separation by ID
@router.get("/{sep_id}", response_model=TeacherSeparationResponse)
def get_separation(sep_id: int, db: Session = Depends(get_db)):
    entry = db.query(TeacherSeparation).filter(
        TeacherSeparation.sep_id == sep_id
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
        db.query(TeacherSeparation)
        .filter(
            TeacherSeparation.sep_id == sep_id,
            TeacherSeparation.status == SeparationStatus.PENDING
        )
        .with_for_update()
        .first()
    )

    if not sep:
        raise HTTPException(404, "Pending separation not found")

    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == sep.teacher_id,
        TeacherMaster.is_active == True
    ).first()

    if not teacher:
        raise HTTPException(400, "Teacher already inactive")

    try:
        # deactivate teacher
        teacher.is_active = False

        # deactivate salary
        db.query(EmployeeSalary).filter(
            EmployeeSalary.employee_type == "teacher",
            EmployeeSalary.employee_id == sep.teacher_id,
            EmployeeSalary.is_active == True
        ).update({"is_active": False})

        # deactivate credentials
        db.query(TeacherCredential).filter(
            TeacherCredential.teacher_id == sep.teacher_id,
            TeacherCredential.is_active == True
        ).update({"is_active": False})

        # update separation
        sep.status = SeparationStatus.APPROVED
        sep.approved_at = datetime.now(timezone.utc)
        sep.academic_session_id = session.session_id

        db.commit()

        return {
            "message": "Teacher separation approved",
            "teacher_id": sep.teacher_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

# endpoint to reject a request
@router.post("/reject/{sep_id}")
def reject_separation(sep_id: int, payload: RejectSeparationRequest, db: Session = Depends(get_db)):

    sep = db.query(TeacherSeparation).filter(
        TeacherSeparation.sep_id == sep_id,
        TeacherSeparation.status == SeparationStatus.PENDING
    ).first()

    if not sep:
        raise HTTPException(404, "Pending separation not found")

    sep.status = SeparationStatus.REJECTED
    sep.remarks = payload.reason
    sep.rejected_at = datetime.now(timezone.utc)

    db.commit()

    return {"message": "Separation rejected"}
