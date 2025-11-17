from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.payment_method import PaymentMethod
from Backends.Backend_admin.schemas.fees_schemas import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
    PaymentMethodResponse
)

router = APIRouter(
    prefix="/admin/payment-methods",
    tags=["Admin Payment Method Management"]
)

# ----Payment Methods----
# endpoint to create/add payment methods
@router.post("/", response_model=PaymentMethodResponse, status_code=201)
def create_payment_method(payload: PaymentMethodCreate, db: Session = Depends(get_db)):
    # Check duplicate method name
    exists = db.query(PaymentMethod).filter(
        PaymentMethod.method_name == payload.method_name
    ).first()

    if exists:
        raise HTTPException(400, detail="Payment method already exists")

    method = PaymentMethod(
        method_name=payload.method_name,
        is_active=True
    )

    db.add(method)
    db.commit()
    db.refresh(method)
    return method

# endpoint to get single payment method using method id
@router.get("/{method_id}", response_model=PaymentMethodResponse)
def get_payment_method(method_id: int, db: Session = Depends(get_db)):
    method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()
    
    if not method:
        raise HTTPException(404, "Payment method not found")
    
    return method

# endpoint to view all payment methods
@router.get("/", response_model=list[PaymentMethodResponse])
def get_all_payment_methods(db: Session = Depends(get_db)):
    return db.query(PaymentMethod).order_by(PaymentMethod.method_id).all()

# endpoint to update a payment method
@router.put("/{method_id}", response_model=PaymentMethodResponse)
def update_payment_method(
    method_id: int,
    payload: PaymentMethodUpdate,
    db: Session = Depends(get_db)
):
    method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()

    if not method:
        raise HTTPException(404, "Payment method not found")

    if payload.method_name:
        # Check duplicate
        duplicate = db.query(PaymentMethod).filter(
            PaymentMethod.method_name == payload.method_name,
            PaymentMethod.method_id != method_id
        ).first()

        if duplicate:
            raise HTTPException(400, "Another payment method with this name already exists")

        method.method_name = payload.method_name

    if payload.is_active is not None:
        method.is_active = payload.is_active

    db.commit()
    db.refresh(method)
    return method

# endpoint to delete a payment method
@router.delete("/{method_id}", status_code=204)
def delete_payment_method(method_id: int, db: Session = Depends(get_db)):
    method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()

    if not method:
        raise HTTPException(404, "Payment method not found")

    # Soft delete: just disable
    method.is_active = False

    db.commit()
    return
