# Backends/Shared/models/staff_master.py

from sqlalchemy import Integer, String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base

class StaffMaster(Base):
    __tablename__ = "staff_master"

    staff_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    
    experience_years: Mapped[int] = mapped_column(Integer, default=0)

    # relationships
    separation_ref = relationship("StaffSeparation", back_populates="staff")
    transfer_ref = relationship("StaffTransfer", back_populates="staff")
    staff_attendance_records = relationship("StaffAttendance", back_populates="staff")