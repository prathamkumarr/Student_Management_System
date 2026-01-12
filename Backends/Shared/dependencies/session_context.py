from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from Backends.Shared.connection import get_db
from Backends.Shared.models.academic_session import AcademicSession

def get_current_session(db: Session = Depends(get_db)) -> AcademicSession:
    session = db.query(AcademicSession).filter(
        AcademicSession.is_active == True
    ).first()

    if not session:
        raise HTTPException(
            status_code=500,
            detail="No active academic session configured"
        )

    return session
