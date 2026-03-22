from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..base import Base


class Role(Base):
    __tablename__ = "roles"

    RoleId = Column(Integer, primary_key=True, index=True)
    RoleName = Column(String, unique=True, index=True)
    Description = Column(String, nullable=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
