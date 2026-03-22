from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..base import Base


class School(Base):
    __tablename__ = "schools"

    SchoolId = Column(Integer, primary_key=True, index=True)
    SchoolName = Column(String, unique=True, index=True)
    Address = Column(String)
    PhoneNumber = Column(String)
    Email = Column(String, unique=True, index=True)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
