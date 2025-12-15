from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class ActivityStudentMap(Base):
    __tablename__ = "activity_student_map"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activity_master.activity_id", ondelete="CASCADE")
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students_master.student_id", ondelete="CASCADE")
    )

    __table_args__ = (
        UniqueConstraint("activity_id", "student_id", name="uq_activity_student"),
    )
