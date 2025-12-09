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
    subject_id: Optional[int] = Query(None, description="Optional subject filter"),
    db: Session = Depends(get_db)
):
    """
    Read-only work list for a student.
    - Uses student_id -> class_id
    - Returns all work for that class
    - Optional ?subject_id= filter
    """

    student = (
        db.query(StudentMaster)
        .filter(StudentMaster.student_id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(404, detail="Student not found")

    q = db.query(WorkRecord).filter(WorkRecord.class_id == student.class_id)

    if subject_id:
        # only apply if WorkRecord has subject_id; if not, remove this filter
        q = q.filter(WorkRecord.subject_id == subject_id)

    recs = q.all()

    result: List[dict] = []
    for r in recs:
        # Try to join subject name if relationship exists; wrapped in try to be safe
        subject_name = None
        try:
            if hasattr(r, "subject_rel") and r.subject_rel:
                subject_name = r.subject_rel.subject_name
        except Exception:
            subject_name = None

        result.append({
            # adjust field names to your WorkRecord model
            "work_id": getattr(r, "work_id", None),
            "class_id": r.class_id,
            "teacher_id": getattr(r, "teacher_id", None),
            "subject_id": getattr(r, "subject_id", None),
            "subject_name": subject_name,
            "title": getattr(r, "title", None),
            "description": getattr(r, "description", None),
            "assigned_date": getattr(r, "assigned_date", None),
            "due_date": getattr(r, "due_date", None),
            "pdf_available": bool(
                getattr(r, "pdf_path", None) or getattr(r, "file_path", None)
            ),
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
