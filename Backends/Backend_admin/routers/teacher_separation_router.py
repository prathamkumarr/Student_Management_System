from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.employee_salary_models import EmployeeSalary
from Backends.Shared.models.teachers_master import TeacherMaster
from Backends.Shared.models.teacher_separation_models import TeacherSeparation
from Backends.Shared.schemas.teacher_separation_schemas import (
    TeacherSeparationCreate, TeacherSeparationResponse
)

router = APIRouter(
    prefix="/admin/teachers/separation",
    tags=["Teacher Separation"]
)

# endpoint to issue separation
@router.post("/issue", response_model=TeacherSeparationResponse)
def issue_separation(payload: TeacherSeparationCreate, db: Session = Depends(get_db)):

    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == payload.teacher_id
    ).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Check if separation already exists
    existing_sep = db.query(TeacherSeparation).filter(
        TeacherSeparation.teacher_id == payload.teacher_id
    ).first()

    if existing_sep:
        raise HTTPException(status_code=400, detail="Separation already issued for this teacher")

    # Mark teacher inactive
    teacher.is_active = False
    db.commit()

    sep_entry = TeacherSeparation(
        teacher_id=payload.teacher_id,
        reason=payload.reason,
        remarks=payload.remarks,
        separation_date=payload.separation_date
    )

    db.add(sep_entry)
    db.commit()
    db.refresh(sep_entry)

    return sep_entry


# endpoint to view all separation requests
@router.get("/all", response_model=list[TeacherSeparationResponse])
def get_all_separations(db: Session = Depends(get_db)):
    entries = db.query(TeacherSeparation).all()
    return entries


# endpoint to view separation by ID
@router.get("/{sep_id}", response_model=TeacherSeparationResponse)
def get_separation(sep_id: int, db: Session = Depends(get_db)):
    entry = db.query(TeacherSeparation).filter(
        TeacherSeparation.sep_id == sep_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Separation record not found")

    return entry

# endpoint to approve separation
@router.post("/approve/{sep_id}")
def approve_separation(sep_id: int, db: Session = Depends(get_db)):

    # Fetch separation record
    sep = db.query(TeacherSeparation).filter(
        TeacherSeparation.sep_id == sep_id
    ).first()

    if not sep:
        raise HTTPException(
            status_code=404,
            detail="Separation record not found"
        )

    # Fetch teacher record
    teacher = db.query(TeacherMaster).filter(
        TeacherMaster.teacher_id == sep.teacher_id
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher record not found"
        )

    # Deactivate teacher
    teacher.is_active = False
    db.commit()

    # Deactivate employee salary for this teacher
    db.query(EmployeeSalary).filter(
        EmployeeSalary.employee_type == "teacher",
        EmployeeSalary.employee_id == sep.teacher_id,
        EmployeeSalary.is_active == True
    ).update({"is_active": False})
    db.commit()

    # Mark separation as approved
    sep.status = True
    db.commit()

    return {
        "message": "Teacher Separation Approved",
        "teacher_id": sep.teacher_id
    }

