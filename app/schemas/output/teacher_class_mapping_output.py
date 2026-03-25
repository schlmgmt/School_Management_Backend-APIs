from pydantic import BaseModel, Field
from datetime import datetime


class TeacherClassMappingResponse(BaseModel):
    """Response schema for teacher-class-section mapping"""
    teacher_class_mapping_id: int = Field(..., alias="TeacherClassMappingId")
    teacher_id: int = Field(..., alias="TeacherId")
    class_id: int = Field(..., alias="ClassId")
    section_id: int = Field(..., alias="SectionId")
    subject: str = Field(..., alias="Subject")
    created_at: datetime = Field(..., alias="CreatedAt")
    updated_at: datetime = Field(..., alias="UpdatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True
