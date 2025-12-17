from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.subjects_master import SubjectMaster
from Backends.Shared.models.student_marks_models import StudentMarks
from Backends.Shared.schemas.student_marks_schemas import StudentMarksCreate, StudentMarksResponse

router = APIRouter(
    prefix="/teacher/results",
    tags=["Teacher - Marks Entry"]
)

# endpoint to ADD MARK FOR ONE STUDENT 
@router.post("/marks/add", response_model=StudentMarksResponse)
def add_marks(payload: StudentMarksCreate, db: Session = Depends(get_db)):

    # Validate student
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == payload.student_id
    ).first()

    if not student:
        raise HTTPException(404, "Student not found")

    # Validate subject
    subject = db.query(SubjectMaster).filter(
        SubjectMaster.subject_id == payload.subject_id
    ).first()

    if not subject:
        raise HTTPException(404, "Subject not found")

    # Check if already exists
    existing = db.query(StudentMarks).filter(
        StudentMarks.student_id == payload.student_id,
        StudentMarks.subject_id == payload.subject_id,
        StudentMarks.exam_id == payload.exam_id
    ).first()

    if existing:
        raise HTTPException(400, "Marks already entered for this student in this exam")

    # Insert marks
    entry = StudentMarks(
        student_id=payload.student_id,
        subject_id=payload.subject_id,
        exam_id=payload.exam_id,
        marks_obtained=payload.marks_obtained,
        max_marks=payload.max_marks,
        remarks=payload.remarks
    )

    # auto pass/fail logic
    entry.is_pass = payload.marks_obtained >= (0.33 * payload.max_marks)

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


# endpoint to VIEW ALL MARKS FOR EXAM 
@router.get("/marks/exam/{exam_id}")
def get_marks_for_exam(exam_id: int, db: Session = Depends(get_db)):

    entries = db.query(StudentMarks).filter(
        StudentMarks.exam_id == exam_id
    ).all()

    return entries
