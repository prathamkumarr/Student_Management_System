from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster

router = APIRouter(
    prefix="/admin/students",
    tags=["Admin - Students"]
)

@router.get("/")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(StudentMaster).all()
    return [
        {
            "student_id": s.student_id,
            "full_name": s.full_name,
            "class_id": s.class_id
        }
        for s in students
    ]
