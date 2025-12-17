from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.subjects_master import SubjectMaster

router = APIRouter(prefix="/admin/teachers", tags=["Teachers"])

@router.get("/{teacher_id}")
def get_teacher_details(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(TeacherMaster).filter(TeacherMaster.teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(404, detail="Teacher not found")

    subject = db.query(SubjectMaster).filter(SubjectMaster.subject_id == teacher.subject_id).first()

    return {
        "teacher_id": teacher.teacher_id,
        "full_name": teacher.full_name,
        "subject_id": teacher.subject_id,
        "subject_name": subject.subject_name if subject else None
    }


@router.get("/")
def get_all_teachers(db: Session = Depends(get_db)):
    teachers = (
        db.query(TeacherMaster, SubjectMaster)
        .outerjoin(
            SubjectMaster,
            TeacherMaster.subject_id == SubjectMaster.subject_id
        )
        .all()
    )

    return [
        {
            "teacher_id": t.teacher_id,
            "full_name": t.full_name,
            "subject_id": t.subject_id,
            "subject_name": s.subject_name if s else None
        }
        for t, s in teachers
    ]
