from sqlalchemy import Integer, String, Date, DateTime, Enum, ForeignKey, func, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Backends.Shared.base import Base
from Backends.Shared.enums.attendance_enums import AttendanceStatus

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
    status = mapped_column(Enum(AttendanceStatus), nullable=False)
    academic_session_id = mapped_column(
        Integer,
        ForeignKey("academic_session.session_id"),
        nullable=False,
        index=True
    )
    remarks: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at:Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    is_active = mapped_column(Boolean, default=True)

    # relationships
    staff = relationship("StaffMaster", back_populates="staff_attendance_records")
