from pydantic import BaseModel, EmailStr
from typing import Optional


class SchoolCreateRequest(BaseModel):
    school_name: str
    address: str
    phone_number: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "school_name": "St. Mary's School",
                "address": "123 Main Street, City",
                "phone_number": "555-1234",
                "email": "contact@stmarys.com"
            }
        }


class SchoolUpdateRequest(BaseModel):
    school_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        json_schema_extra = {
            "example": {
                "school_name": "St. Mary's School Updated",
                "address": "456 New Street, City",
                "phone_number": "555-5678",
                "email": "newemail@stmarys.com"
            }
        }


class SchoolStatusRequest(BaseModel):
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_active": True
            }
        }
