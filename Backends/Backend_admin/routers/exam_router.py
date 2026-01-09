from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.exam_master import ExamMaster
from Backends.Shared.schemas.exam_schemas import ExamCreate, ExamResponse, ExamUpdate
from Backends.Shared.models.result_models import ResultMaster

router = APIRouter(
    prefix="/admin/exams",
    tags=["Exams"]
)

# endpoint to CREATE EXAM 
@router.post("/create", response_model=ExamResponse)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db)):
    exists = db.query(ExamMaster).filter(
        ExamMaster.exam_name == payload.exam_name.strip().upper(),
        ExamMaster.exam_date == payload.exam_date
    ).first()

    if exists:
        raise HTTPException(
        status_code=400,
        detail="Exam with same name and date already exists"
        )
    
    exam_name = payload.exam_name.strip().upper()
    new_exam = ExamMaster(
        exam_name=exam_name,
        description=payload.description,
        exam_date=payload.exam_date
    )

    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return new_exam


# endpoint to VIEW ALL EXAMS 
@router.get("/all", response_model=list[ExamResponse])
def get_all_exams(db: Session = Depends(get_db)):
    return db.query(ExamMaster).filter(ExamMaster.is_active == True).all()


# endpoint to VIEW EXAM BY ID 
@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(ExamMaster).filter(ExamMaster.exam_id == exam_id).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    return exam


# endpoint to UPDATE EXAM 
@router.put("/update/{exam_id}", response_model=ExamResponse)
def update_exam(exam_id: int, payload: ExamUpdate, db: Session = Depends(get_db)):

    exam = db.query(ExamMaster).filter(
        ExamMaster.exam_id == exam_id,
        ExamMaster.is_active == True
    ).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    # extract updates FIRST
    updates = payload.model_dump(exclude_unset=True)

    # normalize exam_name if present
    if "exam_name" in updates:
        updates["exam_name"] = updates["exam_name"].strip().upper()

    # duplicate check (name + date combo)
    if "exam_name" in updates or "exam_date" in updates:
        exists = db.query(ExamMaster).filter(
            ExamMaster.exam_name == updates.get("exam_name", exam.exam_name),
            ExamMaster.exam_date == updates.get("exam_date", exam.exam_date),
            ExamMaster.exam_id != exam_id,
            ExamMaster.is_active == True
        ).first()

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Duplicate exam name and date"
            )

    # apply updates
    for k, v in updates.items():
        setattr(exam, k, v)

    db.commit()
    db.refresh(exam)

    return exam


# endpoint to DELETE EXAM
@router.delete("/delete/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)):

    exam = db.query(ExamMaster).filter(
        ExamMaster.exam_id == exam_id
    ).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    used = db.query(ResultMaster).filter(
        ResultMaster.exam_id == exam_id
        ).first()

    if used:
        raise HTTPException(
        400,
        "Cannot delete exam - results already exist"
        )

    exam.is_active = False
    db.commit()

    return {"message": "Exam deleted successfully", "exam_id": exam_id}

# ----------------------
@router.get("/")
def get_exams(db: Session = Depends(get_db)):
    exams = db.query(ExamMaster).filter(ExamMaster.is_active == True).all()
    return [
        {
            "exam_id": e.exam_id,
            "exam_name": e.exam_name
        }
        for e in exams
    ]