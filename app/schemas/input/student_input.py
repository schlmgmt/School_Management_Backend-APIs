from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class StudentCreateRequest(BaseModel):
    student_name: str
    email: EmailStr
    class_id: int
    section_id: int
    roll_number: str
    fathers_name: str
    mothers_name: str
    phone_number: str
    sec_phone_number: Optional[str] = None
    date_of_birth: date
    admission_date: date

    class Config:
        json_schema_extra = {
            "example": {
                "student_name": "John Doe",
                "email": "john@example.com",
                "class_id": 10,
                "section_id": 1,
                "roll_number": "A001",
                "fathers_name": "James Doe",
                "mothers_name": "Jane Doe",
                "phone_number": "555-1234",
                "sec_phone_number": "555-5678",
                "date_of_birth": "2008-05-15",
                "admission_date": "2020-06-01"
            }
        }


class StudentUpdateRequest(BaseModel):
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    roll_number: Optional[str] = None
    fathers_name: Optional[str] = None
    mothers_name: Optional[str] = None
    phone_number: Optional[str] = None
    sec_phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    admission_date: Optional[date] = None

    class Config:
        json_schema_extra = {
            "example": {
                "class_id": 11,
                "roll_number": "A002",
                "phone_number": "555-9999"
            }
        }


class StudentStatusRequest(BaseModel):
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_active": True
            }
        }
