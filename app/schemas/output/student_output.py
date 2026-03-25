from pydantic import BaseModel
from datetime import datetime, date


class StudentResponse(BaseModel):
    student_id: int
    user_id: int
    email: str
    class_id: int
    section_id: int
    roll_number: str
    fathers_name: str
    mothers_name: str
    phone_number: str
    sec_phone_number: str = None
    date_of_birth: date
    admission_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
