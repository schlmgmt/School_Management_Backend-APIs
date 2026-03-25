from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TeacherClassMappingCreateRequest(BaseModel):
    """Request schema for creating teacher-class-section mapping"""
    teacher_id: int = Field(..., description="Teacher ID")
    class_id: int = Field(..., description="Class ID")
    section_id: int = Field(..., description="Section ID")
    subject: str = Field(..., min_length=1, max_length=200, description="Subject to teach in this class-section")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "teacher_id": 1,
                "class_id": 1,
                "section_id": 1,
                "subject": "Mathematics"
            }
        }
    }


class TeacherClassMappingResponse(BaseModel):
    """Response schema for teacher-class-section mapping"""
    teacher_class_mapping_id: int = Field(..., alias="TeacherClassMappingId")
    teacher_id: int = Field(..., alias="TeacherId")
    class_id: int = Field(..., alias="ClassId")
    section_id: int = Field(..., alias="SectionId")
    created_at: datetime = Field(..., alias="CreatedAt")
    updated_at: datetime = Field(..., alias="UpdatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True
