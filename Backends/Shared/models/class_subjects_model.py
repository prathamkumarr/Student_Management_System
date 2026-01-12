from sqlalchemy import Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class ClassSubject(Base):
    __tablename__ = "class_subjects"

    __table_args__ = (
        UniqueConstraint(
            "class_id",
            "subject_id",
            name="uq_class_subject"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    class_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("classes_master.class_id"),
        nullable=False
    )

    subject_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subjects_master.subject_id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # optional relationships (useful later)
    class_obj = relationship(
        "ClassMaster",
        back_populates="class_subjects"
    )

    subject = relationship(
        "SubjectMaster",
        back_populates="class_subjects"
    )
