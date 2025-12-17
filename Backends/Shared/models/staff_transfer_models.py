from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base


class StaffTransfer(Base):
    __tablename__ = "staff_transfers"

    transfer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    staff_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("staff_master.staff_id"), nullable=False
    )

    # Previous (old) details
    old_department: Mapped[str] = mapped_column(String(120))
    old_role: Mapped[str] = mapped_column(String(120))

    # Updated (new) details
    new_department: Mapped[str] = mapped_column(String(120), nullable=True)
    new_role: Mapped[str] = mapped_column(String(120), nullable=True)

    request_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[bool] = mapped_column(default=False)   

    staff = relationship("StaffMaster", back_populates="transfer_ref")
