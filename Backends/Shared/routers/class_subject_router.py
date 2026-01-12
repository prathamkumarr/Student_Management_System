from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.class_subjects_model import ClassSubject
from Backends.Shared.models.subjects_master import SubjectMaster

router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)


@router.get("/{class_id}/subjects")
def get_subjects_for_class(class_id: int, db: Session = Depends(get_db)):

    subjects = (
        db.query(
            SubjectMaster.subject_id,
            SubjectMaster.subject_name
        )
        .join(
            ClassSubject,
            ClassSubject.subject_id == SubjectMaster.subject_id
        )
        .filter(
            ClassSubject.class_id == class_id,
            ClassSubject.is_active == True
        )
        .all()
    )

    if not subjects:
        raise HTTPException(
            status_code=404,
            detail="No subjects assigned to this class"
        )

    return [
        {
            "subject_id": s.subject_id,
            "subject_name": s.subject_name
        }
        for s in subjects
    ]
