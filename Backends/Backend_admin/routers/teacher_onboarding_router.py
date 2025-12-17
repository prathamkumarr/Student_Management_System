# Backends/Backend_admin/routers/teacher_onboarding_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.teacher_onboarding_models import TeacherOnboarding
from Backends.Shared.schemas.teacher_onboarding_schemas import (
    TeacherOnboardingCreate, TeacherOnboardingResponse
)
from Backends.Shared.models.teachers_master import TeacherMaster

router = APIRouter(
    prefix="/admin/teachers/onboardings",
    tags=["Teacher Onboarding"]
)

# endpoint to CREATE ONBOARDING 
@router.post("/create", response_model=TeacherOnboardingResponse)
def create_onboarding(payload: TeacherOnboardingCreate, db: Session = Depends(get_db)):
    new_entry = TeacherOnboarding(**payload.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


# endpoint to VIEW ALL ONBOARDINGS 
@router.get("/all", response_model=list[TeacherOnboardingResponse])
def get_all_onboardings(db: Session = Depends(get_db)):
    return db.query(TeacherOnboarding).all()


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
def approve_onboarding(onboarding_id: int, db: Session = Depends(get_db)):

    entry = db.query(TeacherOnboarding).filter(
        TeacherOnboarding.onboarding_id == onboarding_id
    ).first()

    if not entry:
        raise HTTPException(404, "Onboarding request not found")

    # Create teacher account
    new_teacher = TeacherMaster(
        full_name=entry.full_name,
        date_of_birth=entry.date_of_birth,
        gender=entry.gender,
        address=entry.address,
        email=entry.email,
        phone=entry.phone,
        subject_id=entry.subject_id,
        qualification=entry.qualification,
        experience_years=entry.experience_years
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    # Delete onboarding request
    db.delete(entry)
    db.commit()

    return {
        "message": "Teacher onboarded successfully!",
        "teacher_id": new_teacher.teacher_id
    }
