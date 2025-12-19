from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from Backends.Shared.models.credentials_models import (
    StudentCredential,
    TeacherCredential,
    StaffCredential
)

router = APIRouter(prefix="/auth", tags=["Login"])

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    # Student Login
    stu = db.query(StudentCredential).filter_by(
        login_email=email,
        login_password=password
    ).first()

    if stu:
        return {"role": "student", "id": stu.student_id}

    # Teacher Login
    t = db.query(TeacherCredential).filter_by(
        login_email=email,
        login_password=password
    ).first()

    if t:
        return {"role": "teacher", "id": t.teacher_id}

    # Staff Login
    st = db.query(StaffCredential).filter_by(
        login_email=email,
        login_password=password
    ).first()

    if st:
        return {"role": "staff", "id": st.staff_id}

    raise HTTPException(status_code=401, detail="Invalid Login Credentials")
