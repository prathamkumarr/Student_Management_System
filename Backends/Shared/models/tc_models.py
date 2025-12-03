from sqlalchemy import Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column
from Backends.Shared.base import Base

class TransferCertificate(Base):
    __tablename__ = "transfer_certificate"

    tc_id = mapped_column(Integer, primary_key=True, index=True)
    student_id = mapped_column(Integer, ForeignKey("students_master.student_id"), nullable=False)
    issue_date = mapped_column(Date)
    reason = mapped_column(String(255))
    remarks = mapped_column(String(255))
    status = mapped_column(Boolean, default=True)

    student = relationship("StudentMaster", back_populates="tc_ref")
