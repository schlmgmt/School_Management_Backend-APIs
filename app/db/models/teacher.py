from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from ..base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    TeacherId = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, index=True, unique=True)
    Subject = Column(String)
    Qualification = Column(String)
    ExperienceYears = Column(Integer)
    SecPhoneNumber = Column(String, nullable=True)  # Optional
    DateOfBirth = Column(Date)
    JoiningDate = Column(Date)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
