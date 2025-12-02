from typing import Optional
from datetime import date
from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from Backends.Shared.base import Base


class WorkRecord(Base):
    __tablename__ = "work_records"

    work_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    class_id = Column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers_master.teacher_id"), nullable=True)

    subject = Column(String(100), nullable=False)
    work_type = Column(Enum('Classwork', 'Homework', 'Assignment', name="work_type_enum"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)

    file_path = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relationships
    class_ref = relationship("ClassMaster", lazy="joined")
    teacher_ref = relationship("TeacherMaster", lazy="joined")
