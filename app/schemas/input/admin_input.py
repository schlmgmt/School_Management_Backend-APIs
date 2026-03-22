from pydantic import BaseModel, EmailStr


class CreateSchoolAdminRequest(BaseModel):
    admin_name: str
    admin_email: EmailStr
    phone_number: str
    school_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "admin_name": "John Doe",
                "admin_email": "admin@school.com",
                "phone_number": "555-1234",
                "school_id": 1
            }
        }
