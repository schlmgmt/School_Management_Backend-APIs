from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from ..base import Base


class Student(Base):
    __tablename__ = "students"

    StudentId = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, index=True, unique=True)
    ClassId = Column(Integer)
    SectionId = Column(Integer)
    RollNumber = Column(String)
    FathersName = Column(String)
    MothersName = Column(String)
    SecPhoneNumber = Column(String, nullable=True)  # Optional
    DateOfBirth = Column(Date)
    AdmissionDate = Column(Date)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
