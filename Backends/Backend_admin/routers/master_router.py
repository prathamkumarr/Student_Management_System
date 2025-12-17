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
