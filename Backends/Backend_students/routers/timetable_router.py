# Backends/Backend_students/routers/timetable_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.timetable_models import Timetable

router = APIRouter(
    prefix="/student/timetable",
    tags=["Timetable"]
)

@router.get("/{student_id}")
def get_timetable_for_student(
    student_id: int,
    day: Optional[str] = Query(None, description="Optional day filter, e.g. 'Monday'"),
    db: Session = Depends(get_db)
):
    """
    Read-only timetable for a student.
    - Finds the student's class from StudentMaster
    - Returns all timetable rows for that class
    - Optional ?day=Monday filter
    """

    student = (
        db.query(StudentMaster)
        .filter(StudentMaster.student_id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(404, detail="Student not found")

    q = db.query(Timetable).filter(Timetable.class_id == student.class_id)

    if day:
        q = q.filter(Timetable.day == day)

    recs = q.all()

    # Return as simple dicts (doesn't depend on Pydantic schemas)
    result: List[dict] = []
    for r in recs:
        result.append({
            # adjust field names if your model uses different ones
            "timetable_id": getattr(r, "timetable_id", None),
            "class_id": r.class_id,
            "teacher_id": getattr(r, "teacher_id", None),
            "day": getattr(r, "day", None),
            "subject": getattr(r, "subject", None),
            "start_time": getattr(r, "start_time", None),
            "end_time": getattr(r, "end_time", None),
            "room_no": getattr(r, "room_no", None),
        })

    return result
