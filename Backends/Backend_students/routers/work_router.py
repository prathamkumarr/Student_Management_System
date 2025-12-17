# Backends/Backend_students/routers/work_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.work_models import WorkRecord
from Backends.Shared.models.subjects_master import SubjectMaster

router = APIRouter(
    prefix="/student/work",
    tags=["Work"]
)

@router.get("/{student_id}")
def get_work_for_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Student Work Viewer:
    - Finds student → class_id
    - Returns work for that class
    """
    student = (
        db.query(StudentMaster)
        .filter(StudentMaster.student_id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(404, detail="Student not found")

    recs = (
        db.query(WorkRecord)
        .filter(WorkRecord.class_id == student.class_id)
        .all()
    )

    result = []

    for r in recs:
        result.append({
            "work_id": r.work_id,
            "class_id": r.class_id,
            "teacher_id": r.teacher_id,

            "subject": r.subject,

            "title": r.title,
            "description": r.description,
            "due_date": r.due_date,


            "pdf_available": bool(r.file_path),
        })

    return result


@router.get("/download/{work_id}")
def download_work_pdf(
    work_id: int,
    db: Session = Depends(get_db)
):
    """
    Download PDF for a given work.
    Assumes WorkRecord has either `pdf_path` or `file_path` column.
    """

    work = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()

    if not work:
        raise HTTPException(404, detail="Work not found")

    # Try common field names; adjust if your model is different
    file_path = getattr(work, "pdf_path", None) or getattr(work, "file_path", None)

    if not file_path:
        raise HTTPException(
            500,
            detail="No PDF path configured for this work record"
        )

    if not os.path.exists(file_path):
        raise HTTPException(
            404,
            detail="PDF file not found on server"
        )

    filename = os.path.basename(file_path)
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )
