from sqlalchemy import (
    Integer, String, Numeric, DateTime,
    func, UniqueConstraint, ForeignKey,
    CheckConstraint, Boolean, Enum
)
from sqlalchemy.orm import  mapped_column, relationship, Mapped, foreign
from Backends.Shared.base import Base
from Backends.Shared.enums.result_enums import ResultStatus

class ResultMaster(Base):
    __tablename__ = "results_master"
    __table_args__ = (
        UniqueConstraint(
        "student_id",
        "exam_id",
        name="uq_student_exam_result"
        ),
        CheckConstraint("marks_obtained <= max_marks", name="ck_marks_valid"),
    )

    result_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id = mapped_column(Integer, ForeignKey("students_master.student_id"))
    exam_id = mapped_column(Integer, ForeignKey("exams_master.exam_id"))

    total_marks = mapped_column(Numeric(6, 2), nullable=False)
    obtained_marks = mapped_column(Numeric(6, 2), nullable=False)
    percentage = mapped_column(Numeric(5, 2), nullable=False)

    grade = mapped_column(String(5))

    result_status: Mapped[ResultStatus] = mapped_column(
        Enum(ResultStatus),
        default=ResultStatus.PASS,
        nullable=False
    )

    is_active = mapped_column(Boolean, default=True)

    generated_at = mapped_column(DateTime, server_default=func.now())

    # relationships
    marks = relationship(
        "StudentMarks",
        primaryjoin=(
        "and_("
        "ResultMaster.student_id == foreign(StudentMarks.student_id), "
        "ResultMaster.exam_id == foreign(StudentMarks.exam_id)"
        ")"
    ),
    viewonly=True

    )
