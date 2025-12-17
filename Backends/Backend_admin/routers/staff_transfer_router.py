from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.staff_transfer_models import StaffTransfer
from Backends.Shared.schemas.staff_transfer_schemas import (
    StaffTransferCreate, StaffTransferResponse
)

router = APIRouter(prefix="/admin/staff-transfer", tags=["Staff Transfers"])

# endpoint to create a transfer request
@router.post("/request", response_model=StaffTransferResponse)
def create_transfer_request(payload: StaffTransferCreate, db: Session = Depends(get_db)):

    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == payload.staff_id
    ).first()

    if not staff:
        raise HTTPException(404, "Staff member not found")

    # Store current values before change
    transfer_entry = StaffTransfer(
        staff_id=payload.staff_id,
        old_department=staff.department,
        old_role=staff.role,
        new_department=payload.new_department,
        new_role=payload.new_role,
        request_date=payload.request_date
    )

    db.add(transfer_entry)
    db.commit()
    db.refresh(transfer_entry)

    return transfer_entry

# endpoint to view all requests
@router.get("/all", response_model=list[StaffTransferResponse])
def get_all_transfers(db: Session = Depends(get_db)):
    return db.query(StaffTransfer).all()

# endpoint to view a transfer request by ID
@router.get("/{transfer_id}", response_model=StaffTransferResponse)
def get_transfer(transfer_id: int, db: Session = Depends(get_db)):
    tr = db.query(StaffTransfer).filter(
        StaffTransfer.transfer_id == transfer_id
    ).first()

    if not tr:
        raise HTTPException(404, "Transfer record not found")

    return tr

# endpoint to approve a transfer request
@router.post("/approve/{transfer_id}")
def approve_transfer(transfer_id: int, db: Session = Depends(get_db)):

    tr = db.query(StaffTransfer).filter(
        StaffTransfer.transfer_id == transfer_id
    ).first()

    if not tr:
        raise HTTPException(404, "Transfer record not found")

    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == tr.staff_id
    ).first()

    if not staff:
        raise HTTPException(404, "Staff member not found")

    # Update staff details
    if tr.new_department:
        staff.department = tr.new_department

    if tr.new_role:
        staff.role = tr.new_role

    db.commit()

    # Mark transfer as approved
    tr.status = True
    db.commit()

    return {
        "message": "Staff Transfer Approved!",
        "staff_id": tr.staff_id
    }
