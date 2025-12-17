from sqlalchemy import Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class StudentMaster(Base):
    __tablename__ = "students_master"

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    roll_no: Mapped[str] = mapped_column(String(30))
    
    # personal details
    full_name: Mapped[str] = mapped_column(String(120))
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    previous_school: Mapped[str] = mapped_column(String(255), nullable=True)

    # parent details
    father_name: Mapped[str] = mapped_column(String(120), nullable=False)
    mother_name: Mapped[str] = mapped_column(String(120), nullable=True)
    parent_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    parent_email: Mapped[str] = mapped_column(String(120), nullable=True)

    # Academic
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"))
    is_active = mapped_column(Boolean, default=True)

    # relationships
    class_ref = relationship("ClassMaster", back_populates="students")
    attendance_records = relationship( 
        "AttendanceRecord",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    student_fees = relationship("StudentFee", back_populates="student_ref")
    class_ref =relationship("Backends.Shared.models.classes_master.ClassMaster", back_populates="students")
    tc_ref = relationship("TransferCertificate", back_populates="student")
    activities = relationship("ActivityStudentMap", backref="student", cascade="all, delete")
