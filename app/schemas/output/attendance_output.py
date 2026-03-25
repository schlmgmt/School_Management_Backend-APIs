from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List


class AttendanceResponse(BaseModel):
    """Response schema for individual attendance record"""
    attendance_id: int = Field(..., alias="AttendanceId")
    student_id: int = Field(..., alias="StudentId")
    class_id: int = Field(..., alias="ClassId")
    section_id: int = Field(..., alias="SectionId")
    attendance_date: date = Field(..., alias="Date")
    status: str = Field(..., alias="Status")
    marked_by: int = Field(..., alias="MarkedBy")
    created_at: datetime = Field(..., alias="CreatedAt")
    updated_at: datetime = Field(..., alias="UpdatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class BulkAttendanceResponse(BaseModel):
    """Response schema for bulk attendance marking"""
    class_id: int
    section_id: int
    attendance_date: date
    total_marked: int
    attendance_records: List[AttendanceResponse]
