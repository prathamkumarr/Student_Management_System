# Backends/Backend_admin/routers/staff_onboarding_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.staff_onboarding_models import StaffOnboarding
from Backends.Shared.schemas.staff_onboarding_schemas import (
    StaffOnboardingCreate, StaffOnboardingResponse
)
from Backends.Shared.models.staff_master import StaffMaster

router = APIRouter(
    prefix="/admin/staff/onboardings",
    tags=["Staff Onboarding"]
)

# endpoint to CREATE 
@router.post("/create", response_model=StaffOnboardingResponse)
def create_onboarding(payload: StaffOnboardingCreate, db: Session = Depends(get_db)):
    entry = StaffOnboarding(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


# endpoint to VIEW ALL 
@router.get("/all", response_model=list[StaffOnboardingResponse])
def get_all_onboardings(db: Session = Depends(get_db)):
    return db.query(StaffOnboarding).all()


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
def approve_onboarding(onboarding_id: int, db: Session = Depends(get_db)):

    entry = db.query(StaffOnboarding).filter(
        StaffOnboarding.onboarding_id == onboarding_id
    ).first()

    if not entry:
        raise HTTPException(404, "Onboarding request not found")

    # Create StaffMaster entry
    staff = StaffMaster(
        full_name=entry.full_name,
        date_of_birth=entry.date_of_birth,
        gender=entry.gender,
        address=entry.address,
        department=entry.department,
        role=entry.role,
        email=entry.email,              # direct from onboarding
        phone=entry.phone,              # direct from onboarding
        experience_years=entry.experience_years
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    # Remove onboarding request
    db.delete(entry)
    db.commit()

    return {
        "message": "Staff onboarded successfully!",
        "staff_id": staff.staff_id
    }
