from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from ..base import Base


class Section(Base):
    __tablename__ = "sections"

    SectionId = Column(Integer, primary_key=True, index=True)
    ClassId = Column(Integer, ForeignKey("classes.ClassId"), nullable=False, index=True)
    ClassTeacherId = Column(Integer, ForeignKey("teachers.TeacherId"), nullable=False, index=True)
    SectionName = Column(String(100), nullable=False)  # e.g., "A", "B", "C"
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
