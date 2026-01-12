from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from Backends.Shared.models.credentials_models import (
    StudentCredential,
    TeacherCredential,
    StaffCredential
)
from Backends.Shared.models.role_master import RoleMaster

router = APIRouter(prefix="/auth", tags=["Login"])


@router.post("/login", response_model=None)
def login(email: str, password: str, db: Session = Depends(get_db)):

    # ---------- STUDENT ----------
    stu = (
        db.query(StudentCredential, RoleMaster)
        .join(RoleMaster, StudentCredential.role_id == RoleMaster.role_id)
        .filter(
            StudentCredential.login_email == email,
            StudentCredential.login_password == password,
            StudentCredential.is_active == True
        )
        .first()
    )

    if stu:
        student, role = stu
        return {
            "user_id": student.student_id,
            "role": role.role_name
        }

    # ---------- TEACHER ----------
    teacher = (
        db.query(TeacherCredential, RoleMaster)
        .join(RoleMaster, TeacherCredential.role_id == RoleMaster.role_id)
        .filter(
            TeacherCredential.login_email == email,
            TeacherCredential.login_password == password,
            TeacherCredential.is_active == True
        )
        .first()
    )

    if teacher:
        teacher_obj, role = teacher
        return {
            "user_id": teacher_obj.teacher_id,
            "role": role.role_name
        }

    # ---------- STAFF ----------
    staff = (
        db.query(StaffCredential, RoleMaster)
        .join(RoleMaster, StaffCredential.role_id == RoleMaster.role_id)
        .filter(
            StaffCredential.login_email == email,
            StaffCredential.login_password == password,
            StaffCredential.is_active == True
        )
        .first()
    )

    if staff:
        staff_obj, role = staff
        return {
            "user_id": staff_obj.staff_id,
            "role": role.role_name
        }

    raise HTTPException(status_code=401, detail="Invalid login credentials")
