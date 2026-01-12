from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.class_subjects_model import ClassSubject
from Backends.Shared.models.subjects_master import SubjectMaster

router = APIRouter(
    prefix="/students",
    tags=["Student Lookup"]
)

@router.get("/{student_id}/subjects")
def get_subjects_for_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    rows = (
        db.query(SubjectMaster.subject_id, SubjectMaster.subject_name)
        .join(
            ClassSubject,
            ClassSubject.subject_id == SubjectMaster.subject_id
        )
        .filter(
            ClassSubject.class_id == student.class_id,
            ClassSubject.is_active == True
        )
        .order_by(SubjectMaster.subject_name)
        .all()
    )

    return [
        {
            "subject_id": subject_id,
            "subject_name": subject_name
        }
        for subject_id, subject_name in rows
    ]
