from pydantic import BaseModel
from datetime import datetime


class SchoolResponse(BaseModel):
    school_id: int
    school_name: str
    address: str
    phone_number: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
