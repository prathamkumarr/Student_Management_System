# Backends/Backend_admin/routers/fees_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from Backends.Shared.models.students_master import StudentMaster

from Backends.Shared.connection import get_db
from Backends.Shared.models.fees_models import StudentFee
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Shared.schemas.fees_schemas import (
    FeeMasterCreate, FeeMasterResponse, 
    StudentFeeCreate, StudentFeeOut
)

router = APIRouter(prefix="/admin/fees", tags=["Admin Fees Management"])

# endpoint to create fee of a student 
@router.post("/create", response_model=FeeMasterResponse, status_code=status.HTTP_201_CREATED)
def create_fee(payload: FeeMasterCreate, db: Session = Depends(get_db)):
    new_fee = FeeMaster(
        class_id=payload.class_id,
        fee_type=payload.fee_type,
        amount=payload.amount,
        effective_from=payload.effective_from,
        effective_to=payload.effective_to,
        notes=payload.notes,
        is_active=True
    )
    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)
    return new_fee

# endpoint to assign fees to a student 
@router.post("/assign", response_model=StudentFeeOut, status_code=status.HTTP_201_CREATED)
def assign_fee(payload: StudentFeeCreate, db: Session = Depends(get_db)):

    # 1) Check if student exists + active status
    student = db.query(StudentMaster).filter(
        StudentMaster.student_id == payload.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student ID {payload.student_id} not found"
        )

    if student.is_active is False:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot assign fee — Student {payload.student_id} has been issued a TC"
        )

    # 2) Check duplicate / pending fee
    existing = db.query(StudentFee).filter(
        StudentFee.student_id == payload.student_id,
        StudentFee.class_id == payload.class_id,
        StudentFee.fee_id == payload.fee_id,
        StudentFee.status != "paid"
    ).first()

    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Fee already assigned and pending payment"
        )

    # 3) Assign new fee
    new_invoice = StudentFee(
        student_id=payload.student_id,
        class_id=payload.class_id,
        fee_id=payload.fee_id,
        amount_due=payload.amount_due,
        due_date=payload.due_date,
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice

# endpoint to view all fees
@router.get("/", response_model=List[FeeMasterResponse])
def get_all_fees(db: Session = Depends(get_db)):
    fees = db.query(FeeMaster).order_by(FeeMaster.created_at.asc()).all()
    if not fees:
        raise HTTPException(status_code=404, detail="No fee structures found")
    return fees

# Endpoint to fetch fee details using fee_id
@router.get("/get/{fee_id}", response_model=FeeMasterResponse)
def get_fee_by_id(fee_id: int, db: Session = Depends(get_db)):
    fee = db.query(FeeMaster).filter(FeeMaster.fee_id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return fee

# endpoint to update fees using fee_id
@router.put("/update/{fee_id}", response_model=FeeMasterResponse)
def update_fee(fee_id: int, payload: FeeMasterCreate, db: Session = Depends(get_db)):
    fee = db.query(FeeMaster).filter(FeeMaster.fee_id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    fee.fee_type = payload.fee_type
    fee.amount = payload.amount
    fee.effective_from = payload.effective_from
    fee.effective_to = payload.effective_to
    fee.notes = payload.notes

    db.commit()
    db.refresh(fee)
    return fee

# endpoint to delete any fee using fee_id
@router.delete("/delete/{fee_id}", response_model=FeeMasterResponse)
def delete_fee(fee_id: int, db: Session = Depends(get_db)):
    fee = db.query(FeeMaster).filter(FeeMaster.fee_id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    fee.is_active = False  
    db.commit()
    db.refresh(fee)

    return fee   

# endpoint to view all fee history
@router.get("/all", response_model=List[StudentFeeOut])
def get_all_fees(db: Session = Depends(get_db)):
    recs = db.query(StudentFee).all()
    return recs


