from pydantic import BaseModel, Field
from datetime import datetime


class ClassResponse(BaseModel):
    """Response schema for class"""
    class_id: int = Field(..., alias="ClassId")
    school_id: int = Field(..., alias="SchoolId")
    class_name: str = Field(..., alias="ClassName")
    is_active: bool = Field(..., alias="IsActive")
    created_at: datetime = Field(..., alias="CreatedAt")
    updated_at: datetime = Field(..., alias="UpdatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class SectionResponse(BaseModel):
    """Response schema for section"""
    section_id: int = Field(..., alias="SectionId")
    class_id: int = Field(..., alias="ClassId")
    class_teacher_id: int = Field(..., alias="ClassTeacherId")
    section_name: str = Field(..., alias="SectionName")
    is_active: bool = Field(..., alias="IsActive")
    created_at: datetime = Field(..., alias="CreatedAt")
    updated_at: datetime = Field(..., alias="UpdatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True
