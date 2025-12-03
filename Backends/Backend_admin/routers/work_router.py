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

# Save uploads to Assets/work_uploads
UPLOAD_DIR = os.path.join(os.getcwd(), "Assets", "work_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------------ LIST ------------------------
@router.get("/", response_model=List[WorkOut])
def api_list_work(
    class_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(WorkRecord).order_by(WorkRecord.due_date.desc())

    if class_id:
        q = q.filter(WorkRecord.class_id == class_id)
    if teacher_id:
        q = q.filter(WorkRecord.teacher_id == teacher_id)

    records = q.all()

    result = []
    for w in records:
        result.append({
            **w.__dict__,
            "class_name": w.class_ref.class_name if w.class_ref else None,
            "teacher_name": w.teacher_ref.full_name if w.teacher_ref else None
        })

    return result


# ------------------------ GET BY ID ------------------------
@router.get("/{work_id}", response_model=WorkOut)
def api_get_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")
    return {
        **rec.__dict__,
        "class_name": rec.class_ref.class_name if rec.class_ref else None,
        "teacher_name": rec.teacher_ref.full_name if rec.teacher_ref else None
    }


# ------------------------ CREATE (FILE UPLOAD) ------------------------
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
    # Validate PDF only
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    ext = ".pdf"
    dest_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, dest_name)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

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


# Alias: /add (frontend compatibility)
@router.post("/add", response_model=WorkOut, status_code=status.HTTP_201_CREATED)
async def api_create_work_add(
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
    return await api_create_work(
        class_id=class_id,
        work_type=work_type,
        subject=subject,
        title=title,
        description=description,
        due_date=due_date,
        teacher_id=teacher_id,
        file=file,
        db=db
    )


# ------------------------ UPDATE ------------------------
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


# ------------------------ DELETE ------------------------
@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")

    # Delete file if exists
    try:
        if rec.file_path and os.path.exists(rec.file_path):
            os.remove(rec.file_path)
    except:
        pass

    db.delete(rec)
    db.commit()
    return {"message": "Deleted"}


# ------------------------ DOWNLOAD FILE ------------------------
@router.get("/{work_id}/download")
def api_download_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()

    if not rec or not rec.file_path:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(rec.file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(
        rec.file_path,
        media_type="application/pdf",
        filename=os.path.basename(rec.file_path)
    )
