from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base
from Backends.Shared.models.payment_method import PaymentMethod

class StudentMaster(Base):
    __tablename__ = "students_master"

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    roll_no: Mapped[str] = mapped_column(String(30), unique=True)
    full_name: Mapped[str] = mapped_column(String(120))
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes_master.class_id"))

    # relationships
    class_ref = relationship("ClassMaster", back_populates="students")
    attendance_records = relationship("AttendanceRecord", back_populates="student")
    student_fees = relationship("StudentFee", back_populates="student_ref")
    payment_methods: Mapped[list["PaymentMethod"]] = relationship("PaymentMethods", back_populates="student_ref")
    exam_fees =relationship("ExamFeePayment", back_populates="student")