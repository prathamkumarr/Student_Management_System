# Backends/Backend_admin/models/admission_models.py

from sqlalchemy import (
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Backends.Shared.base import Base
from Backends.Shared.enums.admission_enums import AdmissionStatus
from sqlalchemy import Enum as SAEnum
from Backends.Shared.enums.gender_enums import GenderEnum

# -------------------------------
# Student Admission Model
# -------------------------------
class StudentAdmission(Base):
    __tablename__ = "student_admissions"

    # Primary Key
    admission_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # -------------------------------
    # Student Personal Details
    # -------------------------------
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        SAEnum(GenderEnum, name="gender_enum"),
        nullable=False
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    # -------------------------------
    # Parent Details
    # -------------------------------
    father_name: Mapped[str] = mapped_column(String(120), nullable=False)
    mother_name: Mapped[str] = mapped_column(String(120), nullable=True)
    parent_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    parent_email: Mapped[str] = mapped_column(String(120), nullable=True)

    # -------------------------------
    # Academic Details
    # -------------------------------
    class_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("classes_master.class_id"),
        nullable=False
    )
    previous_school: Mapped[str] = mapped_column(String(255), nullable=True)

    # -------------------------------
    # Admission Lifecycle
    # -------------------------------
    status: Mapped[AdmissionStatus] = mapped_column(
        Enum(AdmissionStatus),
        default=AdmissionStatus.DRAFT,
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    submitted_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    verified_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    approved_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    # -------------------------------
    # Student Mapping (after approval)
    # -------------------------------
    student_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("students_master.student_id"),
        nullable=True
    )

    # session
    academic_session_id = mapped_column(
        Integer,
        ForeignKey("academic_session.session_id"),
        nullable=False,
        index=True
    )

    # -------------------------------
    # Meta
    # -------------------------------
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # -------------------------------
    # Relationships
    # -------------------------------
    class_ref = relationship(
        "ClassMaster",
        back_populates="admissions"
    )

    student_ref = relationship(
        "StudentMaster",
        back_populates="admission",
        uselist=False
    )
