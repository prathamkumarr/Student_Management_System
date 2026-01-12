# Backends/Backend_admin/routers/teacher_onboarding_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.teacher_onboarding_models import TeacherOnboarding
from Backends.Shared.schemas.teacher_onboarding_schemas import (
    TeacherOnboardingCreate, TeacherOnboardingResponse
)
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.credentials_models import TeacherCredential
from Backends.Shared.enums.teacher_onboarding_enums import TeacherOnboardingStatus
from Backends.Shared.schemas.teacher_onboarding_schemas import TeacherOnboardingReject
from datetime import datetime, timezone
from Backends.Shared.models.role_master import RoleMaster
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/admin/teachers/onboardings",
    tags=["Teacher Onboarding"],
    dependencies=[Depends(get_current_session)]
)

# endpoint to CREATE ONBOARDING 
@router.post("/create", response_model=TeacherOnboardingResponse)
def create_onboarding(payload: TeacherOnboardingCreate, db: Session = Depends(get_db)):

    # Prevent duplicate onboarding
    existing = db.query(TeacherOnboarding).filter(
        TeacherOnboarding.email == payload.email
    ).first()

    if existing:
        raise HTTPException(400, "Onboarding already exists for this email")

    entry = TeacherOnboarding(
        **payload.model_dump(),
        status=TeacherOnboardingStatus.PENDING
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


# endpoint to VIEW ALL ONBOARDINGS 
@router.get("/all", response_model=list[TeacherOnboardingResponse])
def get_all_onboardings(db: Session = Depends(get_db)):
    return (
        db.query(TeacherOnboarding)
        .filter(TeacherOnboarding.status == TeacherOnboardingStatus.PENDING)
        .order_by(TeacherOnboarding.created_at.desc())
        .all()
    )


# endppont to VIEW ONBOARDING BY ID 
@router.get("/{onboarding_id}", response_model=TeacherOnboardingResponse)
def get_onboarding(onboarding_id: int, db: Session = Depends(get_db)):
    entry = db.query(TeacherOnboarding).filter(
        TeacherOnboarding.onboarding_id == onboarding_id
    ).first()

    if not entry:
        raise HTTPException(404, "Onboarding request not found")

    return entry


# endpoint to APPROVE ONBOARDING 
@router.post("/approve/{onboarding_id}")
def approve_onboarding(
    onboarding_id: int, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

    entry = (
        db.query(TeacherOnboarding)
        .filter(TeacherOnboarding.onboarding_id == onboarding_id)
        .with_for_update()
        .first()
    )

    if not entry:
        raise HTTPException(404, "Onboarding request not found")

    if entry.status != TeacherOnboardingStatus.PENDING:
        raise HTTPException(400, "Only pending onboarding can be approved")

    # Check duplicate teacher
    exists = db.query(TeacherMaster).filter(
        TeacherMaster.email == entry.email,
        TeacherMaster.is_active == True
    ).first()

    if exists:
        raise HTTPException(409, "Teacher already exists")

    try:
        # -----------------------------
        # Create Teacher
        # -----------------------------
        teacher = TeacherMaster(
            full_name=entry.full_name,
            date_of_birth=entry.date_of_birth,
            gender=entry.gender,
            address=entry.address,
            email=entry.email,
            phone=entry.phone,
            subject_id=entry.subject_id,
            qualification=entry.qualification,
            experience_years=entry.experience_years,
            academic_session_id=session.session_id
        )

        db.add(teacher)
        db.flush()

        teacher_role = db.query(RoleMaster).filter(
            RoleMaster.role_name == "teacher"
        ).first()

        if not teacher_role:
            raise HTTPException(500, "Teacher role not configured in role_master")

        # -----------------------------
        # Credentials
        # -----------------------------
        first = entry.full_name.split()[0].lower()
        login_email = f"{teacher.teacher_id}{first}@teacher.school.in"
        password = f"{first[:3]}{teacher.teacher_id}"

        db.add(
            TeacherCredential(
                teacher_id=teacher.teacher_id,
                role_id=teacher_role.role_id,   
                login_email=login_email,
                login_password=password,
                is_active=True
            )
        )

        # -----------------------------
        # Update onboarding status
        # -----------------------------
        entry.status = TeacherOnboardingStatus.APPROVED
        entry.approved_at = datetime.now(timezone.utc)
        entry.academic_session_id = session.session_id

        db.commit()

        return {
            "message": "Teacher onboarded successfully",
            "teacher_id": teacher.teacher_id,
            "login_email": login_email,
            "login_password": password
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

# endpoint to reject a request
@router.post("/reject/{onboarding_id}")
def reject_onboarding(onboarding_id: int, payload: TeacherOnboardingReject, db: Session = Depends(get_db)):

    entry = db.query(TeacherOnboarding).filter(
        TeacherOnboarding.onboarding_id == onboarding_id
    ).first()

    if not entry:
        raise HTTPException(404, "Onboarding not found")

    if entry.status != TeacherOnboardingStatus.PENDING:
        raise HTTPException(400, "Only pending onboarding can be rejected")
    
    if entry.status in (TeacherOnboardingStatus.APPROVED, TeacherOnboardingStatus.REJECTED):
        raise HTTPException(400, "Onboarding already processed")

    entry.status = TeacherOnboardingStatus.REJECTED
    entry.reject_reason = payload.reason
    entry.rejected_at = datetime.now(timezone.utc)

    db.commit()

    return {"message": "Onboarding rejected"}
