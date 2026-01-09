from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.payment_method import PaymentMethod
from Backends.Shared.schemas.fees_schemas import (
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
@router.post("/add", response_model=PaymentMethodResponse, status_code=201)
def create_payment_method(payload: PaymentMethodCreate, db: Session = Depends(get_db)):
    method_name = payload.method_name.strip().upper()
    # Check duplicate method name
    exists = db.query(PaymentMethod).filter(
        PaymentMethod.method_name == method_name
    ).first()

    if exists:
        raise HTTPException(400, detail="Payment method already exists")

    method = PaymentMethod(
        method_name=method_name,
        is_active=True
    )

    db.add(method)
    db.commit()
    db.refresh(method)
    return method

# endpoint to get single payment method using method id
@router.get("/{method_id}", response_model=PaymentMethodResponse)
def get_payment_method(method_id: int, db: Session = Depends(get_db)):
    method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id,
                                            PaymentMethod.is_active == True
                                            ).first()
    
    if not method:
        raise HTTPException(404, "Payment method not found")
    
    return method

# endpoint to view all payment methods
@router.get("/all", response_model=list[PaymentMethodResponse])
def get_all_payment_methods(db: Session = Depends(get_db)):
    return db.query(PaymentMethod).filter(
        PaymentMethod.is_active == True
        ).order_by(PaymentMethod.method_id).all()

# endpoint to update a payment method
@router.put("/update/{method_id}", response_model=PaymentMethodResponse)
def update_payment_method(
    method_id: int,
    payload: PaymentMethodUpdate,
    db: Session = Depends(get_db)
    ):
    method = db.query(PaymentMethod).filter(
        PaymentMethod.method_id == method_id
    ).first()

    if not method:
        raise HTTPException(404, "Payment method not found")

    # ---- NAME UPDATE ----
    if payload.method_name is not None:
        new_name = payload.method_name.strip().upper()

        # duplicate check (excluding self)
        duplicate = db.query(PaymentMethod).filter(
            PaymentMethod.method_name == new_name,
            PaymentMethod.method_id != method_id
        ).first()

        if duplicate:
            raise HTTPException(
                400,
                "Another payment method with this name already exists"
            )

        method.method_name = new_name

    # ---- ACTIVE FLAG UPDATE ----
    if payload.is_active is not None:
        method.is_active = payload.is_active

    db.commit()
    db.refresh(method)
    return method

# endpoint to delete a payment method
@router.delete("/delete/{method_id}", status_code=200)
def delete_payment_method(method_id: int, db: Session = Depends(get_db)):
    method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()

    if not method:
        raise HTTPException(404, "Payment method not found")

    if method.payments:
        raise HTTPException(
        400,
        "Cannot deactivate payment method already used in transactions"
    )

    # Soft delete: just disable
    method.is_active = False
    db.commit()
    db.refresh(method)
    return {"message": "Method Deactivated", "method_id": method_id}
