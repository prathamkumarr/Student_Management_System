from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import distinct

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.models.exam_master import ExamMaster
from Backends.Shared.models.academic_session import AcademicSession
from Backends.Shared.dependencies.session_context import get_current_session

router = APIRouter(
    prefix="/student/exams", tags=["Student Exams"], 
    dependencies=[Depends(get_current_session)]
)

@router.get("/{student_id}")
def get_student_exams(
    student_id: int,
    db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == student_id,
        StudentMaster.is_active == True
    ).first()

    if not student:
        raise HTTPException(404, "Student not found or inactive")

    exams = (
        db.query(
            distinct(ResultMaster.exam_id),
            ExamMaster.exam_name
        )
        .join(
            ExamMaster,
            ExamMaster.exam_id == ResultMaster.exam_id
        )
        .filter(
            ResultMaster.student_id == student_id,
            ResultMaster.academic_session_id == session.session_id,
            ResultMaster.is_active == True,
            ExamMaster.is_active == True
        )
        .order_by(ExamMaster.exam_name.asc())
        .all()
    )

    if not exams:
        return []

    return [
        {
            "exam_id": exam_id,
            "exam_name": exam_name
        }
        for exam_id, exam_name in exams
    ]
