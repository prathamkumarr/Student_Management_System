from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.timetable_models import Timetable
from Backends.Shared.schemas.timetable_schemas import (
    TimetableCreate,
    TimetableUpdate,
    TimetableOut,
)

router = APIRouter(prefix="/admin/timetable", tags=["Admin Timetable"])


@router.get("/", response_model=List[TimetableOut])
def api_list_timetables(class_id: Optional[int] = None, teacher_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    List timetables. Optional filters:
    - class_id: integer
    - teacher_id: integer
    """
    q = db.query(Timetable).order_by(Timetable.class_id, Timetable.day, Timetable.start_time)
    if class_id:
        q = q.filter(Timetable.class_id == class_id)
    if teacher_id:
        q = q.filter(Timetable.teacher_id == teacher_id)
    return q.all()


@router.get("/{timetable_id}", response_model=TimetableOut)
def api_get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    rec = db.query(Timetable).filter(Timetable.timetable_id == timetable_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return rec


@router.post("/", response_model=TimetableOut, status_code=status.HTTP_201_CREATED)
def api_create_timetable(payload: TimetableCreate, db: Session = Depends(get_db)):
    obj = Timetable(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{timetable_id}", response_model=TimetableOut)
def api_update_timetable(timetable_id: int, payload: TimetableUpdate, db: Session = Depends(get_db)):
    rec = db.query(Timetable).filter(Timetable.timetable_id == timetable_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Timetable not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rec, key, value)

    db.commit()
    db.refresh(rec)
    return rec


@router.delete("/{timetable_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    rec = db.query(Timetable).filter(Timetable.timetable_id == timetable_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Timetable not found")
    db.delete(rec)
    db.commit()
    return {"message": "Deleted"}
