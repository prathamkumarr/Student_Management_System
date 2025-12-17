from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.activity_models import ExtraCurricularActivity
from Backends.Shared.models.activity_student_models import ActivityStudentMap
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.students_master import StudentMaster

router = APIRouter(
    prefix="/student/activities",
    tags=["Student - Extra Curricular Activities"]
)


@router.get("/{student_id}")
def get_my_activities(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    rows = (
        db.query(
            ExtraCurricularActivity.activity_id,
            ExtraCurricularActivity.activity_name,
            ExtraCurricularActivity.category,
            TeacherMaster.full_name
        )
        .join(
            ActivityStudentMap,
            ExtraCurricularActivity.activity_id == ActivityStudentMap.activity_id
        )
        .outerjoin(
            TeacherMaster,
            ExtraCurricularActivity.incharge_teacher_id == TeacherMaster.teacher_id
        )
        .filter(ActivityStudentMap.student_id == student_id)
        .order_by(ExtraCurricularActivity.activity_id.desc())
        .all()
    )

    return [
        {
            "activity_id": r.activity_id,
            "activity_name": r.activity_name,
            "category": r.category or "",
            "teacher_name": r.full_name or "N/A"
        }
        for r in rows
    ]
