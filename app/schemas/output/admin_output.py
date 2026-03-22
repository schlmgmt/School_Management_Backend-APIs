from pydantic import BaseModel
from datetime import datetime


class SchoolAdminResponse(BaseModel):
    user_id: int
    user_name: str
    school_id: int
    email: str
    phone_number: str
    role_id: int
    is_password_updated: bool
    created_at: datetime

    class Config:
        from_attributes = True
