from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from Backends.Shared.connection import get_db
from Backends.Shared.models.work_models import WorkRecord
from Backends.Shared.schemas.work_schemas import WorkCreate, WorkUpdate, WorkOut

router = APIRouter(prefix="/admin/work", tags=["Admin Work"])

# Upload folder —  Assets/work_uploads
UPLOAD_DIR = os.path.join(os.getcwd(), "Assets", "work_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=List[WorkOut])
def api_list_work(class_id: Optional[int] = None, teacher_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(WorkRecord).order_by(WorkRecord.due_date.desc())
    if class_id:
        q = q.filter(WorkRecord.class_id == class_id)
    if teacher_id:
        q = q.filter(WorkRecord.teacher_id == teacher_id)
    return q.all()


@router.get("/{work_id}", response_model=WorkOut)
def api_get_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")
    return rec


@router.post("/", response_model=WorkOut, status_code=status.HTTP_201_CREATED)
async def api_create_work(
    class_id: int = Form(...),
    work_type: str = Form(...),
    subject: str = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    due_date: Optional[str] = Form(None),
    teacher_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate extension (allow only PDF)
    filename_lower = file.filename.lower()
    if not filename_lower.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    ext = os.path.splitext(file.filename)[1] or ".pdf"
    dest_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, dest_name)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Build payload using same field names as schema
    payload = WorkCreate(
        class_id=class_id,
        teacher_id=teacher_id,
        subject=subject,
        work_type=work_type,
        title=title,
        description=description,
        due_date=due_date if due_date else None
    )

    obj = WorkRecord(**payload.model_dump(), file_path=dest_path)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{work_id}", response_model=WorkOut)
def api_update_work(work_id: int, payload: WorkUpdate, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rec, key, value)

    db.commit()
    db.refresh(rec)
    return rec


@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")

    # remove file 
    try:
        if rec.file_path and os.path.exists(rec.file_path):
            os.remove(rec.file_path)
    except Exception:
        pass

    db.delete(rec)
    db.commit()
    return {"message": "Deleted"}


@router.get("/{work_id}/download")
def api_download_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec or not rec.file_path:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(rec.file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(rec.file_path, media_type="application/pdf", filename=os.path.basename(rec.file_path))
