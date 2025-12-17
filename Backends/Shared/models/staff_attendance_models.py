from sqlalchemy import Integer, String, Date, DateTime, Enum, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base

class StaffAttendance(Base):
    __tablename__ = "staff_attendance"
    __table_args__ = (
            UniqueConstraint("staff_id", "date", name="uq_staff_date"),
        )

    record_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey("staff_master.staff_id"), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    check_in: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    check_out: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(Enum("P", "A", "L", name="staff_attendance_status"), nullable=False)
    remarks: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at:Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # relationships
    staff = relationship("StaffMaster", back_populates="staff_attendance_records")
