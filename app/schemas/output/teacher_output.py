from pydantic import BaseModel
from datetime import datetime, date


class TeacherResponse(BaseModel):
    teacher_id: int
    user_id: int
    email: str
    subject: str
    qualification: str
    experience_years: int
    phone_number: str
    sec_phone_number: str = None
    date_of_birth: date
    joining_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
