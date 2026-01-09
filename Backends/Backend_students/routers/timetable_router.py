# Backends/Backend_students/routers/timetable_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from Backends.Shared.connection import get_db
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.timetable_models import Timetable
from Backends.Shared.models.teachers_master import TeacherMaster

router = APIRouter(prefix="/student/timetable", tags=["Timetable"])

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

    q = (
        db.query(
            Timetable,
            TeacherMaster.full_name.label("teacher_name")
        )
        .join(TeacherMaster, Timetable.teacher_id == TeacherMaster.teacher_id)
        .filter(Timetable.class_id == student.class_id)
    )


    if day:
        q = q.filter(Timetable.day == day)

    recs = q.all()

    # Return as simple dicts 
    result: List[dict] = []

    for timetable, teacher_name in recs:
        result.append({
            "timetable_id": timetable.timetable_id,
            "class_id": timetable.class_id,
            "teacher_name": teacher_name,
            "day": timetable.day,
            "subject": timetable.subject,
            "start_time": timetable.start_time,
            "end_time": timetable.end_time,
            "room_no": timetable.room_no,
        })


    return result
