from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base
from Backends.Shared.models.students_master import StudentMaster
from Backends.Shared.models.fees_master import FeeMaster
from Backends.Shared.models.exam_fee_master import ExamFeeMaster

class ClassMaster(Base):
    __tablename__ = "classes_master"

    class_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_name: Mapped[str] = mapped_column(String(50))
    section: Mapped[str] = mapped_column(String(10))

    # Relationships
    attendance_records = relationship("AttendanceRecord", back_populates="class_ref")
    students: Mapped[list["StudentMaster"]] = relationship("StudentMaster", back_populates="class_ref")
    fees: Mapped[list["FeeMaster"]] = relationship("FeeMaster", back_populates="class_ref")
    student_fees = relationship("StudentFee", back_populates="class_Ref")
    exam_fee: Mapped[list["ExamFeeMaster"]] = relationship("ExamFeeMaster", back_populates="class_ref")