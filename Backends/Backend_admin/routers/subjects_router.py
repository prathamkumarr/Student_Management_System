from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.subjects_master import SubjectMaster

router = APIRouter(
    prefix="/admin/subjects",
    tags=["Admin Subjects"]
)


@router.get("/")
def get_subjects(db: Session = Depends(get_db)):
    rows = db.query(SubjectMaster).all()
    return [
        {
            "subject_id": r.subject_id,
            "subject_name": r.subject_name
        }
        for r in rows
    ]
