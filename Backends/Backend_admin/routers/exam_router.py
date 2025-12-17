from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.exam_master import ExamMaster
from Backends.Shared.schemas.exam_schemas import ExamCreate, ExamResponse, ExamUpdate

router = APIRouter(
    prefix="/admin/exams",
    tags=["Exams"]
)

# endpoint to CREATE EXAM 
@router.post("/create", response_model=ExamResponse)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db)):

    new_exam = ExamMaster(
        exam_name=payload.exam_name,
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
    return db.query(ExamMaster).all()


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
    exam = db.query(ExamMaster).filter(ExamMaster.exam_id == exam_id).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    exam.exam_name = payload.exam_name
    exam.description = payload.description
    exam.exam_date = payload.exam_date

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

    db.delete(exam)
    db.commit()

    return {"message": "Exam deleted successfully", "exam_id": exam_id}
