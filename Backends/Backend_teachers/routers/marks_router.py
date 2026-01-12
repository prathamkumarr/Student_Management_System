from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.subjects_master import SubjectMaster
from Backends.Shared.models.student_marks_models import StudentMarks
from Backends.Shared.models.exam_master import ExamMaster
from Backends.Shared.models.class_subjects_model import ClassSubject
from Backends.Shared.schemas.student_marks_schemas import (
    StudentMarksCreate, StudentMarksResponse,
    StudentMarksBulkCreate, StudentMarksUpdate
)
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession

router = APIRouter(
    prefix="/teacher/results",
    tags=["Teacher - Marks Entry"],
    dependencies=[Depends(get_current_session)]
)

# endpoint to ADD MARK FOR ONE STUDENT 
@router.post("/marks/add", response_model=StudentMarksResponse)
def add_marks(
    payload: StudentMarksCreate, db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):

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
    
    exists = db.query(ClassSubject).filter(
        ClassSubject.class_id == student.class_id,
        ClassSubject.subject_id == payload.subject_id,
        ClassSubject.is_active == True
    ).first()

    if not exists:
        raise HTTPException(
        status_code=400,
        detail="Subject not assigned to student's class"
        )
    
    exam = db.query(ExamMaster).filter(
        ExamMaster.exam_id == payload.exam_id
        ).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

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
        academic_session_id=session.session_id,
        remarks=payload.remarks
    )

    PASS_PERCENTAGE = 0.33
    entry.is_pass = payload.marks_obtained >= (PASS_PERCENTAGE * payload.max_marks)

    db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
        status_code=400,
        detail="Marks already entered for this student in this exam"
        )
    db.refresh(entry)

    return entry


# endpoint to VIEW ALL MARKS with filters
@router.get("/marks", response_model=List[StudentMarksResponse])
def get_marks(
    exam_id: Optional[int] = Query(None),
    student_id: Optional[int] = Query(None),
    subject_id: Optional[int] = Query(None),
    class_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(StudentMarks)

    # ---- Dynamic filters ----
    if exam_id is not None:
        query = query.filter(StudentMarks.exam_id == exam_id)

    if student_id is not None:
        query = query.filter(StudentMarks.student_id == student_id)

    if subject_id is not None:
        query = query.filter(StudentMarks.subject_id == subject_id)

    if class_id is not None:
        query = query.join(StudentMaster).filter(
            StudentMaster.class_id == class_id
        )

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No marks found for given filters"
        )

    return results


# endpoint to update marks of a student
@router.put("/marks/{mark_id}", response_model=StudentMarksResponse)
def update_marks(
    mark_id: int,
    payload: StudentMarksUpdate,
    db: Session = Depends(get_db)
):
    entry = db.get(StudentMarks, mark_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Marks record not found"
        )

    # ---------- VALIDATION ----------
    if payload.marks_obtained > payload.max_marks:
        raise HTTPException(
            status_code=400,
            detail="Marks obtained cannot exceed max marks"
        )

    # ---------- UPDATE ----------
    entry.marks_obtained = payload.marks_obtained
    entry.max_marks = payload.max_marks
    entry.remarks = payload.remarks

    PASS_PERCENTAGE = 0.33
    entry.is_pass = (
        payload.marks_obtained >= PASS_PERCENTAGE * payload.max_marks
    )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to update marks"
        )

    db.refresh(entry)
    return entry


@router.get("/marks/filter")
def filter_marks_for_update(
    class_id: int,
    subject_id: int,
    exam_id: int,
    db: Session = Depends(get_db)
):
    entries = db.query(StudentMarks).join(StudentMaster).filter(
        StudentMaster.class_id == class_id,
        StudentMarks.subject_id == subject_id,
        StudentMarks.exam_id == exam_id
    ).all()

    if not entries:
        raise HTTPException(
            status_code=404,
            detail="No marks found for selected criteria"
        )

    return entries


# endpoint to enter marks in bulk
@router.post("/marks/add-bulk", status_code=201)
def add_marks_bulk(
    payload: StudentMarksBulkCreate,
    db: Session = Depends(get_db),
    session: AcademicSession = Depends(get_current_session)
):
    # ---- Validate subject ----
    subject = db.query(SubjectMaster).filter(
        SubjectMaster.subject_id == payload.subject_id
    ).first()

    if not subject:
        raise HTTPException(404, "Subject not found")

    # ---- Validate exam ----
    exam = db.query(ExamMaster).filter(
        ExamMaster.exam_id == payload.exam_id
    ).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    # ---- Validate subject-class mapping ----
    mapping = db.query(ClassSubject).filter(
        ClassSubject.class_id == payload.class_id,
        ClassSubject.subject_id == payload.subject_id,
        ClassSubject.is_active == True
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=400,
            detail="Subject not assigned to this class"
        )

    # ---- Fetch students of class ----
    students = db.query(StudentMaster).filter(
        StudentMaster.class_id == payload.class_id,
        StudentMaster.is_active == True
    ).all()

    if not students:
        raise HTTPException(404, "No students found in this class")

    student_map = {s.student_id: s for s in students}

    inserted = 0
    skipped = []

    PASS_PERCENTAGE = 0.33

    for item in payload.marks:

        student = student_map.get(item.student_id)
        if not student:
            skipped.append(item.student_id)
            continue

        # ---- Check duplicate ----
        exists = db.query(StudentMarks).filter(
            StudentMarks.student_id == item.student_id,
            StudentMarks.subject_id == payload.subject_id,
            StudentMarks.exam_id == payload.exam_id
        ).first()

        if exists:
            skipped.append(item.student_id)
            continue

        entry = StudentMarks(
            student_id=item.student_id,
            subject_id=payload.subject_id,
            exam_id=payload.exam_id,
            marks_obtained=item.marks_obtained,
            max_marks=payload.max_marks,
            academic_session_id=session.session_id,
            remarks=payload.remarks,
            is_pass=item.marks_obtained >= (PASS_PERCENTAGE * payload.max_marks)
        )

        db.add(entry)
        inserted += 1

    if inserted == 0:
        raise HTTPException(
            status_code=400,
            detail="No marks were inserted (duplicates or invalid students)"
        )

    db.commit()

    return {
        "message": "Bulk marks entry completed",
        "inserted": inserted,
        "skipped_student_ids": skipped
    }
