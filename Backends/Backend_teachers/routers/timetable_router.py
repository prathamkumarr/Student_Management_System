from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.timetable_models import Timetable
from Backends.Shared.models.classes_master import ClassMaster

router = APIRouter(prefix="/teacher/timetable", tags=["Teacher Timetable"])


@router.get("/{teacher_id}")
def get_teacher_timetable(teacher_id: int, db: Session = Depends(get_db)):

    rows = (
        db.query(
            Timetable,
            ClassMaster.class_name,
            ClassMaster.section
        )
        .join(ClassMaster, ClassMaster.class_id == Timetable.class_id)
        .filter(Timetable.teacher_id == teacher_id)
        .all()
    )

    result = []
    for t, class_name, section in rows:
        result.append({
            "timetable_id": t.timetable_id,
            "class_id": t.class_id,
            "class_name": class_name,
            "section": section,
            "day": t.day,
            "subject": t.subject,
            "start_time": str(t.start_time),
            "end_time": str(t.end_time),
            "room_no": t.room_no
        })

    return result
