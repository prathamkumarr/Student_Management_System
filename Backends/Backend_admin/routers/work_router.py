from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from Backends.Shared.connection import get_db
from Backends.Shared.models.work_models import WorkRecord
from Backends.Shared.schemas.work_schemas import WorkCreate, WorkUpdate, WorkOut, WorkFilter
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.teachers_master import TeacherMaster

router = APIRouter(prefix="/admin/work", tags=["Admin Work"])

UPLOAD_DIR = os.path.join(os.getcwd(), "Assets", "work_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ======================================================
#  LIST ALL WORK 
# ======================================================
@router.get("/", response_model=List[WorkOut])
def api_list_work(
    class_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(WorkRecord).order_by(WorkRecord.work_type.desc())

    if class_id:
        q = q.filter(WorkRecord.class_id == class_id)
    if teacher_id:
        q = q.filter(WorkRecord.teacher_id == teacher_id)

    records = q.all()
    result = []

    for w in records:
        class_name = getattr(w.class_ref, "class_name", None)
        section = getattr(w.class_ref, "section", None)
        teacher_name = getattr(w.teacher_ref, "full_name", None)

        result.append({
            "work_id": w.work_id,
            "class_id": w.class_id,
            "class_name": class_name,
            "section": section,
            "teacher_id": w.teacher_id,
            "teacher_name": teacher_name,
            "subject": w.subject,
            "work_type": w.work_type,
            "title": w.title,
            "description": w.description,
            "due_date": w.due_date,
            "file_path": w.file_path,
            "created_at": w.created_at,
            "updated_at": w.updated_at
        })

    return result


# ======================================================
#  CREATE (UPLOAD)  
# ======================================================
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
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    dest_name = f"{uuid.uuid4().hex}.pdf"
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


# ======================================================
#  ADD 
# ======================================================
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


# ======================================================
#  FILTER  
# ======================================================
@router.post("/filter")
def api_filter_work(payload: WorkFilter, db: Session = Depends(get_db)):
    q = (
        db.query(
            WorkRecord,
            ClassMaster.class_name,
            ClassMaster.section,
            TeacherMaster.full_name
        )
        .join(ClassMaster, WorkRecord.class_id == ClassMaster.class_id)
        .outerjoin(TeacherMaster, WorkRecord.teacher_id == TeacherMaster.teacher_id)
    )

    # CLASS FILTER
    if payload.class_id:
        q = q.filter(WorkRecord.class_id == payload.class_id)

    elif payload.class_name:
        parts = payload.class_name.split()
        if len(parts) >= 2:
            section = parts[-1]
            base_name = " ".join(parts[:-1])
            q = q.filter(ClassMaster.class_name == base_name)
            q = q.filter(ClassMaster.section == section)
        else:
            q = q.filter(ClassMaster.class_name == payload.class_name)

    if payload.section:
        q = q.filter(ClassMaster.section == payload.section)

    if payload.teacher_id:
        q = q.filter(WorkRecord.teacher_id == payload.teacher_id)
    elif payload.teacher_name:
        q = q.filter(TeacherMaster.full_name == payload.teacher_name)

    if payload.subject:
        q = q.filter(WorkRecord.subject == payload.subject)

    if payload.work_type:
        q = q.filter(WorkRecord.work_type == payload.work_type)

    rows = q.order_by(WorkRecord.due_date.desc()).all()

    result = []
    for w, class_name, section, teacher_name in rows:
        result.append({
            "work_id": w.work_id,
            "class_id": w.class_id,
            "class_name": class_name,
            "section": section,
            "teacher_id": w.teacher_id,
            "teacher_name": teacher_name or None,
            "subject": w.subject,
            "work_type": w.work_type,
            "title": w.title,
            "description": w.description,
            "due_date": w.due_date,
            "file_path": w.file_path,
            "created_at": w.created_at,
            "updated_at": w.updated_at
        })

    return result


# ======================================================
#  DOWNLOAD  
# ======================================================
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


# ======================================================
#  GET BY ID  
# ======================================================
@router.get("/{work_id}", response_model=WorkOut)
def api_get_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")

    return {
        **rec.__dict__,
        "class_name": rec.class_ref.class_name if rec.class_ref else None,
        "section": rec.class_ref.section if rec.class_ref else None,
        "teacher_name": rec.teacher_ref.full_name if rec.teacher_ref else None
    }


# ======================================================
#  UPDATE
# ======================================================
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


# ======================================================
#  DELETE
# ======================================================
@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_work(work_id: int, db: Session = Depends(get_db)):
    rec = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Work not found")

    if rec.file_path and os.path.exists(rec.file_path):
        try:
            os.remove(rec.file_path)
        except:
            pass

    db.delete(rec)
    db.commit()
    return {"message": "Deleted"}
