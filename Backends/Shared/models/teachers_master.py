from sqlalchemy import Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class TeacherMaster(Base):
    __tablename__ = "teachers_master"

    teacher_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # personal details
    full_name: Mapped[str] = mapped_column(String(120))
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)

    # job details
    subject_id: Mapped[int] = mapped_column(Integer)  
    class_id: Mapped[int] = mapped_column(Integer)  
    department: Mapped[str] = mapped_column(String(120), nullable=True)  
    qualification: Mapped[str] = mapped_column(String(120), nullable=True)
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    # session
    academic_session_id = mapped_column(
        Integer,
        ForeignKey("academic_session.session_id"),
        nullable=False,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # relationships
    student_attendance_records = relationship("AttendanceRecord", back_populates="teacher")
    teacher_attendance_records = relationship("TeacherAttendance", back_populates="teacher")
    separation_ref = relationship("TeacherSeparation", back_populates="teacher")
    transfer_ref = relationship("TeacherTransfer", back_populates="teacher")
