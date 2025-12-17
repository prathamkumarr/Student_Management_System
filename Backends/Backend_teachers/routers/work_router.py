from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from Backends.Shared.connection import get_db
from Backends.Shared.models.work_models import WorkRecord
from Backends.Shared.schemas.work_schemas import WorkUpdate


router = APIRouter(prefix="/teacher/work", tags=["Teacher Work"])


# ALIAS: /teacher/work/add  (required by frontend)
# -------------------------------------------------------------
@router.post("/add")
def teacher_add_work_alias(
    class_id: int = Form(...),
    teacher_id: int = Form(...),
    subject: str = Form(...),
    work_type: str = Form(...),
    title: str = Form(...),
    description: str = Form(None),
    due_date: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return teacher_add_work(
        class_id=class_id,
        teacher_id=teacher_id,
        subject=subject,
        work_type=work_type,
        title=title,
        description=description,
        due_date=due_date,
        file=file,
        db=db
    )


# MAIN CREATE ROUTE: /teacher/work/
# -------------------------------------------------------------
@router.post("/")
def teacher_add_work(
    class_id: int = Form(...),
    teacher_id: int = Form(...),
    subject: str = Form(...),
    work_type: str = Form(...),
    title: str = Form(...),
    description: str = Form(None),
    due_date: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # save file
    folder = "uploaded_work"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # save db record
    new_work = WorkRecord(
        class_id=class_id,
        teacher_id=teacher_id,
        subject=subject,
        work_type=work_type,
        title=title,
        description=description,
        due_date=due_date,
        file_path=file_path,
    )

    db.add(new_work)
    db.commit()
    db.refresh(new_work)

    return {"message": "Work added", "work_id": new_work.work_id}


# GET ALL WORK OF THIS TEACHER
# -------------------------------------------------------------
@router.get("/{teacher_id}")
def get_teacher_work(teacher_id: int, db: Session = Depends(get_db)):

    recs = (
        db.query(WorkRecord)
        .filter(WorkRecord.teacher_id == teacher_id)
        .all()
    )

    result = []
    for r in recs:
        cls = r.class_ref
        teacher = r.teacher_ref

        result.append({
            "work_id": r.work_id,
            "class_id": r.class_id,
            "class_name": cls.class_name if cls else None,
            "section": cls.section if cls else None,
            "teacher_id": r.teacher_id,
            "teacher_name": teacher.full_name if teacher else None,
            "subject": r.subject,
            "work_type": r.work_type,
            "title": r.title,
            "description": r.description,
            "due_date": str(r.due_date),
            "pdf_path": r.file_path,
        })

    return result


# UPDATE WORK 
# -------------------------------------------------------------
@router.put("/{work_id}")
def update_work(work_id: int, update_data: WorkUpdate, db: Session = Depends(get_db)):
    work = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()

    if not work:
        raise HTTPException(404, "Work not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(work, field, value)

    db.commit()
    db.refresh(work)
    return work


# DELETE WORK
# -------------------------------------------------------------
@router.delete("/{work_id}")
def delete_work(work_id: int, db: Session = Depends(get_db)):
    work = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()

    if not work:
        raise HTTPException(404, "Work not found")

    db.delete(work)
    db.commit()

    return {"message": "Deleted successfully"}


# DOWNLOAD PDF
# -------------------------------------------------------------
@router.get("/download/{work_id}")
def download_teacher_work(work_id: int, db: Session = Depends(get_db)):
    work = db.query(WorkRecord).filter(WorkRecord.work_id == work_id).first()

    if not work:
        raise HTTPException(404, "Work not found")

    if not work.file_path or not os.path.exists(work.file_path):
        raise HTTPException(404, "PDF not found")

    filename = os.path.basename(work.file_path)
    return FileResponse(work.file_path, filename=filename, media_type="application/pdf")
