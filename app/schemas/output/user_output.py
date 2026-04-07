from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    user_id: int = Field(alias="UserId")
    user_name: str = Field(alias="UserName")
    school_id: int = Field(alias="SchoolId")
    class_id: Optional[int] = Field(alias="ClassId")
    section_id: Optional[int] = Field(alias="SectionId")
    role_id: int = Field(alias="RoleId")
    email: str = Field(alias="Email")
    phone_number: Optional[str] = Field(alias="PhoneNumber")
    is_password_updated: bool = Field(alias="IsPasswordUpdated")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
