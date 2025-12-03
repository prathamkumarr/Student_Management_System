from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.timetable_models import Timetable
from Backends.Shared.schemas.timetable_schemas import ( TimetableCreate, TimetableUpdate, TimetableOut,)
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.schemas.timetable_schemas import ( TimetableCreate, TimetableUpdate, TimetableOut, TimetableFilter)

router = APIRouter(prefix="/admin/timetable", tags=["Admin Timetable"])


@router.get("/subjects")
def api_get_subjects(db: Session = Depends(get_db)):
    rows = db.query(Timetable.subject).distinct().all()
    return [r[0] for r in rows]


@router.get("/classes")
def api_get_classes(db: Session = Depends(get_db)):
    rows = db.query(ClassMaster).all()
    return [
        {
            "class_id": r.class_id,
            "class_name": r.class_name,
            "section": r.section
        }
        for r in rows
    ]

@router.get("/teachers")
def api_get_teachers(db: Session = Depends(get_db)):
    rows = db.query(TeacherMaster).all()
    return [
        {
            "teacher_id": r.teacher_id,
            "full_name": r.full_name
        }
        for r in rows
    ]


# ------------------------ LIST ------------------------
@router.get("/", response_model=List[TimetableOut])
def api_list_timetables(
    class_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    subject: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Timetable).order_by(Timetable.class_id, Timetable.day, Timetable.start_time)

    if class_id:
        q = q.filter(Timetable.class_id == class_id)
    if teacher_id:
        q = q.filter(Timetable.teacher_id == teacher_id)
    if subject:
        q = q.filter(Timetable.subject == subject)

    return q.all()

#---------------Filter-----
@router.post("/filter")
def api_filter_timetable(
    payload: TimetableFilter,
    db: Session = Depends(get_db)
):

    q = db.query(
        Timetable,
        ClassMaster.class_name,
        ClassMaster.section,
        TeacherMaster.full_name
    ).join(
        ClassMaster, Timetable.class_id == ClassMaster.class_id
    ).join(
        TeacherMaster, Timetable.teacher_id == TeacherMaster.teacher_id, isouter=True
    )

    if payload.class_id:
        q = q.filter(Timetable.class_id == payload.class_id)

    if payload.teacher_id:
        q = q.filter(Timetable.teacher_id == payload.teacher_id)

    if payload.subject:
        q = q.filter(Timetable.subject == payload.subject)

    rows = q.order_by(Timetable.day, Timetable.start_time).all()

    result = []
    for t, class_name, section, teacher_name in rows:
        result.append({
            "timetable_id": t.timetable_id,
            "day": t.day,
            "class_name": f"{class_name} {section}",
            "subject": t.subject,
            "teacher_name": teacher_name or "N/A",
            "start_time": t.start_time.strftime("%H:%M") if t.start_time else None,
            "end_time": t.end_time.strftime("%H:%M") if t.end_time else None
        })

    return result


# ------------------------ GET BY ID ------------------------
@router.get("/{timetable_id}", response_model=TimetableOut)
def api_get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    rec = db.query(Timetable).filter(Timetable.timetable_id == timetable_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return rec


# ------------------------ CREATE ------------------------
@router.post("/", response_model=TimetableOut, status_code=status.HTTP_201_CREATED)
def api_create_timetable(payload: TimetableCreate, db: Session = Depends(get_db)):
    obj = Timetable(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# Alias for frontend: /add
@router.post("/add", response_model=TimetableOut, status_code=status.HTTP_201_CREATED)
def api_create_timetable_alias(payload: TimetableCreate, db: Session = Depends(get_db)):
    return api_create_timetable(payload, db)


# ------------------------ UPDATE ------------------------
@router.put("/{timetable_id}", response_model=TimetableOut)
def api_update_timetable(
    timetable_id: int,
    payload: TimetableUpdate,
    db: Session = Depends(get_db)
):
    rec = db.query(Timetable).filter(Timetable.timetable_id == timetable_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Timetable not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rec, key, value)

    db.commit()
    db.refresh(rec)
    return rec


# ------------------------ DELETE ------------------------
@router.delete("/{timetable_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    rec = db.query(Timetable).filter(Timetable.timetable_id == timetable_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Timetable not found")

    db.delete(rec)
    db.commit()
    return {"message": "Deleted"}

