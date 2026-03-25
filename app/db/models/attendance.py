from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint, Enum
from datetime import datetime
from ..base import Base
import enum


class AttendanceStatus(str, enum.Enum):
    """Enum for attendance status"""
    PRESENT = "present"
    ABSENT = "absent"


class Attendance(Base):
    __tablename__ = "attendances"

    AttendanceId = Column(Integer, primary_key=True, index=True)
    StudentId = Column(Integer, ForeignKey("students.StudentId"), nullable=False, index=True)
    ClassId = Column(Integer, ForeignKey("classes.ClassId"), nullable=False, index=True)
    SectionId = Column(Integer, ForeignKey("sections.SectionId"), nullable=False, index=True)
    Date = Column(Date, nullable=False, index=True)
    Status = Column(Enum(AttendanceStatus), nullable=False)  # "present" or "absent"
    MarkedBy = Column(Integer, ForeignKey("teachers.TeacherId"), nullable=False, index=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint: Only one attendance record per student per day
    __table_args__ = (
        UniqueConstraint('StudentId', 'Date', name='unique_student_date'),
    )
