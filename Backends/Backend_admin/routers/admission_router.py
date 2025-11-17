# Backends/Backend_admin/routers/admission_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from Backends.Shared.connection import get_db
from Backends.Backend_admin.models.admission_models import StudentAdmission
from Backends.Backend_admin.schemas.admission_schemas import (
    AdmissionCreate, AdmissionResponse
)
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Backend_students.models.fees_models import StudentFee

router = APIRouter(
    prefix="/admin/admissions",
    tags=["Student Admissions"]
)

# endpoint to create new admission
@router.post("/", response_model=AdmissionResponse)
def create_admission(payload: AdmissionCreate, db: Session = Depends(get_db)):
    new_entry = StudentAdmission(**payload.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# endpoint to view all admissions
@router.get("/", response_model=list[AdmissionResponse])
def get_all_admissions(db: Session = Depends(get_db)):
    entries = db.query(StudentAdmission).all()
    return entries

# endpoint to view admission by id
@router.get("/{admission_id}", response_model=AdmissionResponse)
def get_admission(admission_id: int, db: Session = Depends(get_db)):
    entry = db.query(StudentAdmission).filter(
        StudentAdmission.admission_id == admission_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Admission not found")

    return entry

# ----- HELPER FUCNTION ------
def generate_roll_number(db, class_id):
    """Generate next roll number for a given class."""
    from Backends.Backend_students.models import StudentMaster

    last_student = (
        db.query(StudentMaster)
        .filter(StudentMaster.class_id == class_id)
        .order_by(StudentMaster.roll_number.desc())
        .first()
    )

    if last_student and last_student.roll_number:
        return last_student.roll_number + 1

    return 1  # start from roll number 1 for new class

# endpoint to approve an admission request
@router.post("/approve/{admission_id}")
def approve_admission(admission_id: int, db: Session = Depends(get_db)):
    # Step 1 — Fetch admission entry
    entry = db.query(StudentAdmission).filter(
        StudentAdmission.admission_id == admission_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Admission request not found")

    # Step 2 — Convert class_name → class_id
    class_obj = db.query(ClassMaster).filter(
        ClassMaster.class_name == entry.class_name
    ).first()

    if not class_obj:
        raise HTTPException(status_code=400, detail="Invalid class name provided")

    # Step 3 — Create StudentMaster entry
    new_student = StudentMaster(
    full_name=entry.full_name,
    gender=entry.gender,
    dob=entry.dob,
    class_id=class_obj.class_id,
    admission_date=date.today(),
    roll_number=generate_roll_number(db, class_obj.class_id),
    address=entry.address,
    phone=entry.phone,
    email=entry.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    # Step 4 — Auto assign normal fees
    fees = db.query(FeeMaster).filter(
        FeeMaster.class_id == class_obj.class_id,
        FeeMaster.is_active == True
    ).all()

    for f in fees:
        student_fee = StudentFee(
            student_id=new_student.student_id,
            fee_id=f.fee_id,
            status="UNPAID"
        )
        db.add(student_fee)

    db.commit()

    # Step 5 — Auto assign exam fee (if class 10 or 12)
    if class_obj.class_name in ("X", "XII"):
        exam_fee = db.query(FeeMaster).filter(
            FeeMaster.fee_type == "Board Exam Fee",
            FeeMaster.class_id == class_obj.class_id,
            FeeMaster.is_active == True
        ).first()

        if exam_fee:
            db.add(StudentFee(student_id=new_student.student_id, fee_id=exam_fee.fee_id))

        db.commit()

    # Step 6 — Delete admission form (optional)
    db.delete(entry)
    db.commit()

    return {"message": "Admission approved successfully!", "student_id": new_student.student_id}
