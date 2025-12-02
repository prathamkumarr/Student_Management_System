from sqlalchemy import Column, Integer, String, Time, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from Backends.Shared.base import Base


class Timetable(Base):
    __tablename__ = "timetable"

    timetable_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    class_id = Column(Integer, ForeignKey("classes_master.class_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers_master.teacher_id"), nullable=True)

    day = Column(String(20), nullable=False)
    subject = Column(String(100), nullable=False)

    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    room_no = Column(String(50), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    class_ref = relationship("ClassMaster", lazy="joined")
    teacher_ref = relationship("TeacherMaster", lazy="joined")
