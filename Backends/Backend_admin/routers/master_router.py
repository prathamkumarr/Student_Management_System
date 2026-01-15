from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db

from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.subjects_master import SubjectMaster
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Shared.models.exam_master import ExamMaster
from Backends.Shared.models.result_models import ResultMaster
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.salary_master import SalaryMaster
from Backends.Shared.models.academic_session import AcademicSession


router = APIRouter(prefix="/admin/master", tags=["Master Tables"])


@router.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    return db.query(StudentMaster).all()


@router.get("/classes")
def get_all_classes(db: Session = Depends(get_db)):
    return db.query(ClassMaster).all()


@router.get("/teachers")
def get_all_teachers(db: Session = Depends(get_db)):
    return db.query(TeacherMaster).all()


@router.get("/subjects")
def get_all_subjects(db: Session = Depends(get_db)):
    return db.query(SubjectMaster).all()


@router.get("/fees")
def get_all_fees(db: Session = Depends(get_db)):
    return db.query(FeeMaster).all()


@router.get("/exams")
def get_all_exams(db: Session = Depends(get_db)):
    return db.query(ExamMaster).all()


@router.get("/results")
def get_all_results(db: Session = Depends(get_db)):
    return db.query(ResultMaster).all()


@router.get("/staff")
def get_all_staff(db: Session = Depends(get_db)):
    return db.query(StaffMaster).all()


@router.get("/salary")
def get_all_salary(db: Session = Depends(get_db)):
    return db.query(SalaryMaster).all()


@router.get("/students/class/{class_id}")
def get_students_by_class(class_id: int, db: Session = Depends(get_db)):
    students = (
        db.query(StudentMaster)
        .filter(
            StudentMaster.class_id == class_id,
            StudentMaster.is_active == True
        )
        .all()
    )

    if not students:
        raise HTTPException(
            status_code=404,
            detail="No active students found for this class"
        )

    return [
        {
            "student_id": s.student_id,
            "roll_no": s.roll_no,
            "full_name": s.full_name,
            "class_id": s.class_id
        }
        for s in students
    ]


@router.get("/get/academic-session")
def get_academic_sessions(db: Session = Depends(get_db)):
    sessions = (
        db.query(AcademicSession)
        .order_by(AcademicSession.start_date.desc())
        .all()
    )

    if not sessions:
        raise HTTPException(404, "No academic sessions found")

    return {
        "active_session": next(
            (s for s in sessions if s.is_active), None
        ),
        "all_sessions": sessions
    }


@router.post("/activate/{session_id}")
def activate_academic_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    new_session = db.query(AcademicSession).filter(
        AcademicSession.session_id == session_id
    ).with_for_update().first()

    if not new_session:
        raise HTTPException(404, "Academic session not found")

    if new_session.is_active:
        raise HTTPException(400, "This academic session is already active")

    try:
        # deactivate currently active session
        db.query(AcademicSession).filter(
            AcademicSession.is_active == True
        ).update({"is_active": False})

        # activate selected session
        new_session.is_active = True

        db.commit()

        return {
            "message": "Academic session activated successfully",
            "active_session_id": new_session.session_id,
            "session_name": new_session.session_name
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
