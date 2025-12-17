from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.teacher_transfer_models import TeacherTransfer
from Backends.Shared.schemas.teacher_transfer_schemas import (
    TeacherTransferCreate, TeacherTransferResponse
)

router = APIRouter(prefix="/admin/teacher-transfer", tags=["Teacher Transfers"])

# endpoint to create a transfer request
@router.post("/request", response_model=TeacherTransferResponse)
def create_transfer_request(payload: TeacherTransferCreate, db: Session = Depends(get_db)):

    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == payload.teacher_id
    ).first()

    if not teacher:
        raise HTTPException(404, "Teacher not found")

    # Store current values before change
    transfer_entry = TeacherTransfer(
        teacher_id=payload.teacher_id,
        old_department=teacher.department,
        old_subject_id=teacher.subject_id,
        old_class_id=teacher.class_id,
        new_department=payload.new_department,
        new_subject_id=payload.new_subject_id,
        new_class_id=payload.new_class_id,
        request_date=payload.request_date
    )

    db.add(transfer_entry)
    db.commit()
    db.refresh(transfer_entry)

    return transfer_entry

# endpoint to view all requests
@router.get("/all", response_model=list[TeacherTransferResponse])
def get_all_transfers(db: Session = Depends(get_db)):
    return db.query(TeacherTransfer).all()

# endpoint to view a transfer request by ID
@router.get("/{transfer_id}", response_model=TeacherTransferResponse)
def get_transfer(transfer_id: int, db: Session = Depends(get_db)):
    tr = db.query(TeacherTransfer).filter(
        TeacherTransfer.transfer_id == transfer_id
    ).first()

    if not tr:
        raise HTTPException(404, "Transfer record not found")

    return tr

# endpoint to approve a transfer request
@router.post("/approve/{transfer_id}")
def approve_transfer(transfer_id: int, db: Session = Depends(get_db)):

    tr = db.query(TeacherTransfer).filter(
        TeacherTransfer.transfer_id == transfer_id
    ).first()

    if not tr:
        raise HTTPException(404, "Transfer record not found")

    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == tr.teacher_id
    ).first()

    if not teacher:
        raise HTTPException(404, "Teacher not found")

    # Update teacher details
    if tr.new_department:
        teacher.department = tr.new_department

    if tr.new_subject_id is not None:
        teacher.subject_id = tr.new_subject_id

    if tr.new_class_id is not None:   
        teacher.class_id = tr.new_class_id

    db.commit()

    # Mark transfer as approved
    tr.status = True
    db.commit()

    return {
        "message": "Teacher Transfer Approved!",
        "teacher_id": tr.teacher_id
    }
