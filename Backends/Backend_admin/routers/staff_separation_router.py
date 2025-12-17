from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.employee_salary_models import EmployeeSalary
from Backends.Shared.models.staff_master import StaffMaster
from Backends.Shared.models.staff_separation_models import StaffSeparation
from Backends.Shared.schemas.staff_separation_schemas import (
    StaffSeparationCreate, StaffSeparationResponse
)

router = APIRouter(
    prefix="/admin/staff/separation",
    tags=["staff Separation"]
)

# endpoint to issue separation
@router.post("/issue", response_model=StaffSeparationResponse)
def issue_separation(payload: StaffSeparationCreate, db: Session = Depends(get_db)):

    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == payload.staff_id
    ).first()

    if not staff:
        raise HTTPException(status_code=404, detail="staff not found")

    # Check if separation already exists
    existing_sep = db.query(StaffSeparation).filter(
        StaffSeparation.staff_id == payload.staff_id
    ).first()

    if existing_sep:
        raise HTTPException(status_code=400, detail="Separation already issued for this staff member!")

    # Mark staff inactive
    staff.is_active = False
    db.commit()

    sep_entry = StaffSeparation(
        staff_id=payload.staff_id,
        reason=payload.reason,
        remarks=payload.remarks,
        separation_date=payload.separation_date
    )

    db.add(sep_entry)
    db.commit()
    db.refresh(sep_entry)

    return sep_entry


# endpoint to view all separation requests
@router.get("/all", response_model=list[StaffSeparationResponse])
def get_all_separations(db: Session = Depends(get_db)):
    entries = db.query(StaffSeparation).all()
    return entries


# endpoint to view separation by ID
@router.get("/{sep_id}", response_model=StaffSeparationResponse)
def get_separation(sep_id: int, db: Session = Depends(get_db)):
    entry = db.query(StaffSeparation).filter(
        StaffSeparation.sep_id == sep_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Separation record not found")

    return entry

# endpoint to approve separation
@router.post("/approve/{sep_id}")
def approve_separation(sep_id: int, db: Session = Depends(get_db)):

    # Fetch separation record
    sep = db.query(StaffSeparation).filter(
        StaffSeparation.sep_id == sep_id
    ).first()

    if not sep:
        raise HTTPException(
            status_code=404,
            detail="Separation record not found"
        )

    # Fetch staff record
    staff = db.query(StaffMaster).filter(
        StaffMaster.staff_id == sep.staff_id
    ).first()

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="staff record not found"
        )

    # Deactivate staff
    staff.is_active = False
    db.commit()

    # Deactivate employee salary for this staff
    db.query(EmployeeSalary).filter(
        EmployeeSalary.employee_type == "staff",
        EmployeeSalary.employee_id == sep.staff_id,
        EmployeeSalary.is_active == True
    ).update({"is_active": False})
    db.commit()

    # Mark separation as approved
    sep.status = True
    db.commit()

    return {
        "message": "staff Separation Approved",
        "staff_id": sep.staff_id
    }

