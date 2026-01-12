from sqlalchemy import Integer, String, Boolean, Date
from sqlalchemy.orm import mapped_column
from Backends.Shared.base import Base

class AcademicSession(Base):
    __tablename__ = "academic_session"

    session_id = mapped_column(Integer, primary_key=True, index=True)

    # Example: "2024-25"
    session_name = mapped_column(String(20), unique=True, nullable=False)

    start_date = mapped_column(Date, nullable=False)
    end_date   = mapped_column(Date, nullable=False)

    # Only ONE session should be active at a time
    is_active  = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<AcademicSession {self.session_name}>"
