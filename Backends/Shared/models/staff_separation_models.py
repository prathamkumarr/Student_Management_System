from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, Boolean, Enum as SAEnum, func
from sqlalchemy.orm import mapped_column, relationship
from Backends.Shared.base import Base

from Backends.Shared.enums.separation_enums import SeparationStatus


class StaffSeparation(Base):
    __tablename__ = "staff_separation"

    sep_id = mapped_column(Integer, primary_key=True, autoincrement=True)

    staff_id = mapped_column(Integer, ForeignKey("staff_master.staff_id"), nullable=False)

    reason = mapped_column(String(255), nullable=False)
    remarks = mapped_column(String(255), nullable=True)

    separation_date = mapped_column(Date, nullable=False)

    status = mapped_column(
        SAEnum(SeparationStatus, name="staff_separation_status"),
        default=SeparationStatus.PENDING,
        nullable=False
    )

    approved_at = mapped_column(DateTime, nullable=True)
    rejected_at = mapped_column(DateTime, nullable=True)

    created_at = mapped_column(DateTime, server_default=func.now())

    staff = relationship(
        "StaffMaster",
        back_populates="separation_ref"
    )
