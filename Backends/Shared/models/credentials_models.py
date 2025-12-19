from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column
from Backends.Shared.base import Base

class StudentCredential(Base):
    __tablename__ = "student_credentials"

    id = mapped_column(Integer, primary_key=True, index=True)
    student_id = mapped_column(Integer, ForeignKey("students_master.student_id"))
    login_email = mapped_column(String(100), unique=True)
    login_password = mapped_column(String(100))
    is_active = mapped_column(Boolean, default=True)

class TeacherCredential(Base):
    __tablename__ = "teacher_credentials"

    id = mapped_column(Integer, primary_key=True, index=True)
    teacher_id = mapped_column(Integer, ForeignKey("teachers_master.teacher_id"))
    login_email = mapped_column(String(100), unique=True)
    login_password = mapped_column(String(100))
    is_active = mapped_column(Boolean, default=True)

class StaffCredential(Base):
    __tablename__ = "staff_credentials"

    id = mapped_column(Integer, primary_key=True, index=True)
    staff_id = mapped_column(Integer, ForeignKey("staff_master.staff_id"))
    login_email = mapped_column(String(100), unique=True)
    login_password = mapped_column(String(100))
    is_active = mapped_column(Boolean, default=True)
