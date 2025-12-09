from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.work_models import WorkRecord
from Backends.Shared.schemas.work_schemas import WorkCreate, WorkUpdate

router = APIRouter(prefix="/teacher/work", tags=["Teacher Work"])

# CREATE
@router.post("/")
def create_work(work: WorkCreate, db: Session = Depends(get_db)):
    new_work = WorkRecord(**work.dict())
    db.add(new_work)
    db.commit()
    db.refresh(new_work)
    return new_work

# READ ALL for teacher
@router.get("/{teacher_id}")
def get_teacher_work(teacher_id: int, db: Session = Depends(get_db)):
    work = db.query(WorkRecord).filter(WorkRecord.teacher_id == teacher_id).all()
    return work

# UPDATE
@router.put("/{work_id}")
def update_work(work_id: int, update_data: WorkUpdate, db: Session = Depends(get_db)):
    work = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(work, field, value)

    db.commit()
    db.refresh(work)
    return work

# DELETE
@router.delete("/{work_id}")
def delete_work(work_id: int, db: Session = Depends(get_db)):
    work = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    db.delete(work)
    db.commit()
    return {"message": "Deleted successfully"}
