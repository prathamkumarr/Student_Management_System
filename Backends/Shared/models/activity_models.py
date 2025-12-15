from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from Backends.Shared.base import Base

class ExtraCurricularActivity(Base):
    __tablename__ = "activity_master"

    activity_id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    incharge_teacher_id = Column(Integer, ForeignKey("teachers_master.teacher_id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    #relationships
    students = relationship("ActivityStudentMap", backref="activity", cascade="all, delete")
