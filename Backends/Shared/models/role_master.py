from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship
from Backends.Shared.base import Base

class RoleMaster(Base):
    __tablename__ = "role_master"

    role_id = mapped_column(Integer, primary_key=True)
    role_name = mapped_column(String(50), unique=True, nullable=False)

    # relationships
    student = relationship("StudentCredential", back_populates="role")
    teacher = relationship("TeacherCredential", back_populates="role_teacher")
    staff = relationship("StaffCredential", back_populates="role_staff")
