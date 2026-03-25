from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from ..base import Base


class Class(Base):
    __tablename__ = "classes"

    ClassId = Column(Integer, primary_key=True, index=True)
    SchoolId = Column(Integer, ForeignKey("schools.SchoolId"), nullable=False, index=True)
    ClassName = Column(String(100), nullable=False)  # e.g., "10th", "12th"
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
