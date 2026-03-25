from pydantic import BaseModel, Field
from typing import Optional


class ClassCreateRequest(BaseModel):
    """Request schema for creating a class"""
    class_name: str = Field(..., min_length=1, max_length=100, description="Class name (e.g., '10th', '12th')")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "class_name": "10th"
            }
        }
    }


class ClassUpdateRequest(BaseModel):
    """Request schema for updating a class"""
    class_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "class_name": "10th",
                "is_active": True
            }
        }
    }


class ClassStatusRequest(BaseModel):
    """Request schema for toggling class status"""
    is_active: bool = Field(..., description="Set class active or inactive")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "is_active": True
            }
        }
    }


class SectionCreateRequest(BaseModel):
    """Request schema for creating a section"""
    class_id: int = Field(..., description="Class ID to assign section to")
    section_name: str = Field(..., min_length=1, max_length=100, description="Section name (e.g., 'A', 'B', 'C')")
    class_teacher_id: int = Field(..., description="Teacher ID who will be the class teacher for this section")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "class_id": 1,
                "section_name": "A",
                "class_teacher_id": 1
            }
        }
    }


class SectionUpdateRequest(BaseModel):
    """Request schema for updating a section"""
    section_name: Optional[str] = Field(None, min_length=1, max_length=100)
    class_teacher_id: Optional[int] = Field(None, description="Teacher ID to be the class teacher for this section")
    is_active: Optional[bool] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "section_name": "A",
                "class_teacher_id": 1,
                "is_active": True
            }
        }
    }


class SectionStatusRequest(BaseModel):
    """Request schema for toggling section status"""
    is_active: bool = Field(..., description="Set section active or inactive")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "is_active": True
            }
        }
    }
