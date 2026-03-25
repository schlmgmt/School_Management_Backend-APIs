from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class TeacherCreateRequest(BaseModel):
    teacher_name: str
    email: EmailStr
    subject: str
    qualification: str
    experience_years: int
    phone_number: str
    sec_phone_number: Optional[str] = None
    date_of_birth: date
    joining_date: date

    class Config:
        json_schema_extra = {
            "example": {
                "teacher_name": "Mr. Smith",
                "email": "smith@school.com",
                "subject": "Mathematics",
                "qualification": "B.Sc in Mathematics",
                "experience_years": 5,
                "phone_number": "555-1234",
                "sec_phone_number": "555-5678",
                "date_of_birth": "1985-05-15",
                "joining_date": "2018-06-01"
            }
        }


class TeacherUpdateRequest(BaseModel):
    subject: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    phone_number: Optional[str] = None
    sec_phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    joining_date: Optional[date] = None

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Science",
                "experience_years": 6,
                "phone_number": "555-9999"
            }
        }


class TeacherStatusRequest(BaseModel):
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_active": True
            }
        }
