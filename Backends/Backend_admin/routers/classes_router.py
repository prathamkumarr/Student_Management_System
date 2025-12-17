from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.classes_master import ClassMaster

router = APIRouter(
    prefix="/admin/classes",
    tags=["Admin Classes"]
)


@router.get("/")
def get_classes(db: Session = Depends(get_db)):
    rows = db.query(ClassMaster).all()
    return [
        {
            "class_id": r.class_id,
            "class_name": r.class_name,
            "section": r.section
        }
        for r in rows
    ]
