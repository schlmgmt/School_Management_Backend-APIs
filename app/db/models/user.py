from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..base import Base

class User(Base):
    __tablename__ = "users"

    UserId = Column(Integer, primary_key=True, index=True)
    UserName = Column(String)
    SchoolId = Column(Integer, index=True)
    ClassId = Column(Integer)
    SectionId = Column(Integer)
    RoleId = Column(Integer)
    Email = Column(String, unique=True, index=True)
    Password = Column(String)
    PhoneNumber = Column(String)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)

    CreatedBy = Column(Integer)
    UpdatedBy = Column(Integer)

    IsPasswordUpdated = Column(Boolean, default=False)