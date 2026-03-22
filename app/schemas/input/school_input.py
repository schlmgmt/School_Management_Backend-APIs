from pydantic import BaseModel, EmailStr


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
