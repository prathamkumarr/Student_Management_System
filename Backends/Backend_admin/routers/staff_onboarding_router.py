# Backends/Backend_admin/routers/staff_onboarding_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.staff_onboarding_models import StaffOnboarding
from Backends.Shared.schemas.staff_onboarding_schemas import (
    StaffOnboardingCreate, StaffOnboardingResponse
)
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.credentials_models import StaffCredential
from Backends.Shared.enums.staff_onboarding_enums import StaffOnboardingStatus
from Backends.Shared.schemas.staff_onboarding_schemas import StaffOnboardingReject
from datetime import datetime, timezone
from Backends.Shared.models.role_master import RoleMaster
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/admin/staff/onboardings",
    tags=["Staff Onboarding"],
    dependencies=[Depends(get_current_session)]
)

# endpoint to CREATE 
@router.post("/create", response_model=StaffOnboardingResponse)
def create_onboarding(payload: StaffOnboardingCreate, db: Session = Depends(get_db)):

    # Prevent duplicate onboarding
    existing = db.query(StaffOnboarding).filter(
        StaffOnboarding.email == payload.email
    ).first()

    if existing:
        raise HTTPException(400, "Onboarding already exists for this email")

    entry = StaffOnboarding(
        **payload.model_dump(),
        status=StaffOnboardingStatus.PENDING
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


# endpoint to VIEW ALL 
@router.get("/all", response_model=list[StaffOnboardingResponse])
def get_all_onboardings(db: Session = Depends(get_db)):
    return (
        db.query(StaffOnboarding)
        .filter(StaffOnboarding.status == StaffOnboardingStatus.PENDING)
        .order_by(StaffOnboarding.created_at.desc())
        .all()
    )

# endpoint to VIEW BY ID 
@router.get("/{onboarding_id}", response_model=StaffOnboardingResponse)
def get_onboarding(onboarding_id: int, db: Session = Depends(get_db)):
    entry = db.query(StaffOnboarding).filter(
        StaffOnboarding.onboarding_id == onboarding_id
    ).first()

    if not entry:
        raise HTTPException(404, "Onboarding request not found")

    return entry


# endpoint to APPROVE 
@router.post("/approve/{onboarding_id}")
def approve_onboarding(
    onboarding_id: int, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

    entry = (
        db.query(StaffOnboarding)
        .filter(StaffOnboarding.onboarding_id == onboarding_id)
        .with_for_update()
        .first()
    )

    if not entry:
        raise HTTPException(404, "Onboarding request not found")

    if entry.status !=StaffOnboardingStatus.PENDING:
        raise HTTPException(400, "Only pending onboarding can be approved")

    # Check duplicate staff
    exists = db.query(StaffMaster).filter(
        StaffMaster.email == entry.email,
        StaffMaster.is_active == True
    ).first()

    if exists:
        raise HTTPException(409, "Staff already exists")

    try:
        # -----------------------------
        # Create Staff
        # -----------------------------
        staff = StaffMaster(
        full_name=entry.full_name,
        date_of_birth=entry.date_of_birth,
        gender=entry.gender,
        address=entry.address,
        department=entry.department,
        role=entry.role,
        email=entry.email,
        phone=entry.phone,
        experience_years=entry.experience_years,
        academic_session_id=session.session_id
    )

        db.add(staff)
        db.flush()

        staff_role = db.query(RoleMaster).filter(
            RoleMaster.role_name == "staff"
        ).first()

        if not staff_role:
            raise HTTPException(500, "Staff role not configured in role_master")

        # -----------------------------
        # Credentials
        # -----------------------------
        first = entry.full_name.split()[0].lower()
        login_email = f"{staff.staff_id}{first}@staff.school.in"
        password = f"{first[:3]}{staff.staff_id}"

        db.add(
            StaffCredential(
                staff_id=staff.staff_id,
                role_id=staff_role.role_id,   
                login_email=login_email,
                login_password=password,
                is_active=True
            )
        )

        # -----------------------------
        # Update onboarding status
        # -----------------------------
        entry.status = StaffOnboardingStatus.APPROVED
        entry.approved_at = datetime.now(timezone.utc)
        entry.academic_session_id = session.session_id

        db.commit()

        return {
            "message": "Staff onboarded successfully",
            "staff_id": staff.staff_id,
            "login_email": login_email,
            "login_password": password
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
    

# endpoint to reject a request
@router.post("/reject/{onboarding_id}")
def reject_onboarding(onboarding_id: int, payload: StaffOnboardingReject, db: Session = Depends(get_db)):

    entry = db.query(StaffOnboarding).filter(
        StaffOnboarding.onboarding_id == onboarding_id
    ).first()

    if not entry:
        raise HTTPException(404, "Onboarding not found")

    if entry.status != StaffOnboardingStatus.PENDING:
        raise HTTPException(400, "Only pending onboarding can be rejected")
    
    if entry.status in (StaffOnboardingStatus.APPROVED, StaffOnboardingStatus.REJECTED):
        raise HTTPException(400, "Onboarding already processed")

    entry.status = StaffOnboardingStatus.REJECTED
    entry.reject_reason = payload.reason
    entry.rejected_at = datetime.now(timezone.utc)

    db.commit()

    return {"message": "Onboarding rejected"}