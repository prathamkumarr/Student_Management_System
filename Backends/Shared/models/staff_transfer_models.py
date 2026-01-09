from sqlalchemy import Integer, String, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backends.Shared.base import Base
from sqlalchemy import Enum as SAEnum
from Backends.Shared.enums.transfer_enums import TransferStatus

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
    status = mapped_column(
        SAEnum(TransferStatus, name="staff_transfer_status_enum"),
        default=TransferStatus.PENDING,
        nullable=False
    )
    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )
    approved_at = mapped_column(DateTime, nullable=True)
    rejected_at = mapped_column(DateTime, nullable=True)
    reject_reason = mapped_column(String(255), nullable=True)

    # relationship
    staff = relationship("StaffMaster", back_populates="transfer_ref")
