from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base
from Backends.Shared.models.admission_models import StudentAdmission

class ClassMaster(Base):
    __tablename__ = "classes_master"

    class_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_name: Mapped[str] = mapped_column(String(50))
    section: Mapped[str] = mapped_column(String(10))

    # Relationships
    attendance_records = relationship("AttendanceRecord", back_populates="class_ref")
    students = relationship("StudentMaster", back_populates="class_ref")

    fees = relationship("Backends.Shared.models.fees_master.FeeMaster", back_populates="class_ref")
    student_fees = relationship("Backends.Shared.models.fees_models.StudentFee", back_populates="class_ref")

    admissions: Mapped[list["StudentAdmission"]] = relationship(
        "StudentAdmission",
        back_populates="class_ref"
    )

