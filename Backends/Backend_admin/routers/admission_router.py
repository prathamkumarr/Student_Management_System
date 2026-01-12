from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date, timezone
from decimal import Decimal

from Backends.Shared.connection import get_db
from Backends.Shared.models.admission_models import StudentAdmission
from Backends.Shared.enums.admission_enums import AdmissionStatus
from Backends.Shared.schemas.admission_schemas import (
    AdmissionCreate, AdmissionResponse, AdmissionReject
)
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.classes_master import ClassMaster
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Shared.models.fees_models import StudentFee
from Backends.Shared.models.credentials_models import StudentCredential
from Backends.Shared.enums.student_fees_enums import StudentFeeStatus
from Backends.Shared.models.role_master import RoleMaster
from Backends.Shared.dependencies.session_context import get_current_session
from Backends.Shared.models.academic_session import AcademicSession


router = APIRouter(
    prefix="/admin/admissions",
    tags=["Student Admissions"],
    dependencies=[Depends(get_current_session)]
)

# endpoint to create new admission
@router.post("/create", response_model=AdmissionResponse)
def create_admission(payload: AdmissionCreate, db: Session = Depends(get_db)):
    new_entry = StudentAdmission(
        **payload.model_dump(),
        status=AdmissionStatus.DRAFT
        )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# endpoint to view all admissions
@router.get("/all", response_model=list[AdmissionResponse])
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

# endpoint to Submit Admission
@router.patch("/{admission_id}/submit", response_model=AdmissionResponse)
def submit_admission(admission_id: int, db: Session = Depends(get_db)):

    entry = db.get(StudentAdmission, admission_id)

    if not entry:
        raise HTTPException(404, "Admission not found")

    if entry.status != AdmissionStatus.DRAFT:
        raise HTTPException(400, "Only draft admissions can be submitted")

    entry.status = AdmissionStatus.SUBMITTED
    entry.submitted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(entry)

    return entry

# endpoint to Verify Admission
@router.patch("/{admission_id}/verify", response_model=AdmissionResponse)
def verify_admission(admission_id: int, db: Session = Depends(get_db)):

    entry = db.get(StudentAdmission, admission_id)

    if not entry:
        raise HTTPException(404, "Admission not found")

    if entry.status != AdmissionStatus.SUBMITTED:
        raise HTTPException(400, "Admission not in submitted state")

    entry.status = AdmissionStatus.VERIFIED
    entry.verified_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(entry)

    return entry

# endpoint to Reject Admission
@router.patch("/{admission_id}/reject", response_model=AdmissionResponse)
def reject_admission(admission_id: int, payload: AdmissionReject, db: Session = Depends(get_db)):
    entry = db.get(StudentAdmission, admission_id)

    if not entry:
        raise HTTPException(404, "Admission not found")

    if entry.status not in (
        AdmissionStatus.SUBMITTED,
        AdmissionStatus.VERIFIED
    ):
        raise HTTPException(400, "Admission cannot be rejected now")

    entry.status = AdmissionStatus.REJECTED
    entry.remarks = payload.remarks

    db.commit()
    db.refresh(entry)

    return entry

# ----- HELPER FUCNTION ------
def generate_roll_number(db, class_id):
    """
    Generate roll number for mid-session admission.
    Rule: always assign next roll at the end (MAX + 1).
    """

    last_roll = (
        db.query(StudentMaster.roll_no)
        .filter(
            StudentMaster.class_id == class_id,
            StudentMaster.roll_no.isnot(None)
        )
        .order_by(StudentMaster.roll_no.desc())
        .first()
    )

    if not last_roll or not last_roll[0]:
        return 1

    return last_roll[0] + 1

# endpoint to Approve Admission
@router.post("/{admission_id}/approve")
def approve_admission(
    admission_id: int, db: Session = Depends(get_db), 
    session: AcademicSession = Depends(get_current_session)
):

    entry = (
        db.query(StudentAdmission)
        .filter(StudentAdmission.admission_id == admission_id)
        .with_for_update()
        .first()
    )

    if not entry:
        raise HTTPException(404, "Admission not found")
    
    if entry.gender is None:
        raise HTTPException(400, "Gender missing in admission")

    if entry.status != AdmissionStatus.VERIFIED:
        raise HTTPException(400, "Admission not ready for approval")

    if entry.student_id:
        raise HTTPException(409, "Admission already approved")

    class_obj = db.get(ClassMaster, entry.class_id)
    if not class_obj:
        raise HTTPException(400, "Invalid class")

    try:
        # -----------------------------
        # Create Student
        # -----------------------------
        new_student = StudentMaster(
            roll_no=generate_roll_number(db, class_obj.class_id),
            full_name=entry.full_name,
            date_of_birth=entry.date_of_birth,
            gender=entry.gender,
            address=entry.address,
            previous_school=entry.previous_school,
            father_name=entry.father_name,
            mother_name=entry.mother_name,
            parent_phone=entry.parent_phone,
            parent_email=entry.parent_email,
            class_id=class_obj.class_id,
            academic_session_id=session.session_id
        )
        db.add(new_student)
        db.flush() 

        student_role = db.query(RoleMaster).filter(
            RoleMaster.role_name == "student"
        ).first()

        if not student_role:
            raise HTTPException(500, "Student role not configured in role_master")

        # -----------------------------
        # Credentials
        # -----------------------------
        first = entry.full_name.split()[0].lower()
        email = f"{new_student.student_id}{first}{entry.parent_phone[-2:]}@student.school.in"
        password = (first[:3] if len(first) >= 3 else first) + str(new_student.student_id)

        db.add(
            StudentCredential(
                student_id=new_student.student_id,
                role_id=student_role.role_id,
                login_email=email,
                login_password=password,
                is_active=True
            )
        )

        # -----------------------------
        # Fees mapping
        # -----------------------------
        fees = db.query(FeeMaster).filter(
            FeeMaster.class_id == class_obj.class_id,
            FeeMaster.is_mandatory == False,
            FeeMaster.is_active == True
        ).all()

        for f in fees:
            db.add(
                StudentFee(
                    student_id=new_student.student_id,
                    class_id=class_obj.class_id,
                    fee_id=f.fee_id,
                    amount_due=Decimal(f.amount),
                    amount_paid=Decimal("0.00"),
                    status=StudentFeeStatus.PENDING,
                    due_date=f.effective_to or date.today()
                )
            )

        # -----------------------------
        # Exam fee
        # -----------------------------
        if class_obj.class_name in ("X", "XII"):
            exam_fee = db.query(FeeMaster).filter(
                FeeMaster.fee_type == "Board Exam Fee",
                FeeMaster.class_id == class_obj.class_id,
                FeeMaster.is_active == True
            ).first()

            if exam_fee:
                db.add(
                    StudentFee(
                        student_id=new_student.student_id,
                        class_id=class_obj.class_id,
                        fee_id=exam_fee.fee_id,
                        amount_due=Decimal(exam_fee.amount),
                        amount_paid=Decimal("0.00"),
                        status=StudentFeeStatus.PENDING, 
                        due_date=exam_fee.effective_to or date.today()
                    )
                )
        
        # -----------------------------
        # Mandatory fees (AUTO ASSIGN)
        # -----------------------------
        mandatory_fees = db.query(FeeMaster).filter(
            FeeMaster.class_id == class_obj.class_id,
            FeeMaster.is_mandatory == True,
            FeeMaster.is_active == True
        ).all()

        for f in mandatory_fees:

            # avoid duplicate assignment (extra safety)
            existing_fee = db.query(StudentFee).filter(
                StudentFee.student_id == new_student.student_id,
                StudentFee.fee_id == f.fee_id,
                StudentFee.is_active == True
            ).first()

            if existing_fee:
                continue

            db.add(
                StudentFee(
                    student_id=new_student.student_id,
                    class_id=class_obj.class_id,
                    fee_id=f.fee_id,
                    amount_due=Decimal(f.amount),
                    amount_paid=Decimal("0.00"),
                    due_date=f.effective_to or date.today(),
                    status=StudentFeeStatus.PENDING
                )
            )
        
        # -----------------------------
        # Update Admission
        # -----------------------------
        entry.student_id = new_student.student_id
        entry.status = AdmissionStatus.APPROVED
        entry.academic_session_id = session.session_id
        entry.approved_at = datetime.now(timezone.utc)

        db.commit()

        return {
            "message": "Admission approved successfully",
            "student_id": new_student.student_id,
            "login_email": email,
            "login_password": password
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

