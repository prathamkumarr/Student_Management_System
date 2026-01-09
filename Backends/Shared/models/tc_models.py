from sqlalchemy import Integer, String, Date, ForeignKey, Boolean, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship, mapped_column
from Backends.Shared.base import Base

class TransferCertificate(Base):
    __tablename__ = "transfer_certificate"
    __table_args__ = (
        UniqueConstraint("student_id", name="uq_student_tc"),
    )

    tc_id = mapped_column(Integer, primary_key=True, index=True)
    student_id = mapped_column(Integer, ForeignKey("students_master.student_id"), nullable=False)
    issue_date = mapped_column(Date)
    reason = mapped_column(String(255))
    remarks = mapped_column(String(255))
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    student = relationship("StudentMaster", back_populates="tc_ref")
