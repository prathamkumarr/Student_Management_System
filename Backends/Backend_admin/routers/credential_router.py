from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backends.Shared.connection import get_db
from Backends.Shared.models.credentials_models import (
    StudentCredential,
    TeacherCredential,
    StaffCredential
)

credential_router = APIRouter(
    prefix="/admin/credentials",
    tags=["Admin Credentials"]
)

@credential_router.get("/students")
def get_student_credentials(db: Session = Depends(get_db)):
    records = db.query(StudentCredential).all()

    return [
        {
            "id": r.id,
            "student_id": r.student_id,
            "login_email": r.login_email,
            "login_password": r.login_password,
            "is_active": r.is_active
        }
        for r in records
    ]

@credential_router.get("/teachers")
def get_teacher_credentials(db: Session = Depends(get_db)):
    records = db.query(TeacherCredential).all()

    return [
        {
            "id": r.id,
            "teacher_id": r.teacher_id,
            "login_email": r.login_email,
            "login_password": r.login_password,
            "is_active": r.is_active
        }
        for r in records
    ]

@credential_router.get("/staff")
def get_staff_credentials(db: Session = Depends(get_db)):
    records = db.query(StaffCredential).all()

    return [
        {
            "id": r.id,
            "staff_id": r.staff_id,
            "login_email": r.login_email,
            "login_password": r.login_password,
            "is_active": r.is_active
        }
        for r in records
    ]
