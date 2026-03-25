from pydantic import BaseModel
from datetime import date
from typing import Literal, List


class StudentAttendanceEntry(BaseModel):
    """Schema for individual student attendance entry"""
    student_id: int
    status: Literal["present", "absent"]


class AttendanceMarkRequest(BaseModel):
    """Request schema for marking attendance for multiple students"""
    class_id: int
    section_id: int
    date: date
    students: List[StudentAttendanceEntry]


class AttendanceUpdateRequest(BaseModel):
    """Request schema for updating attendance"""
    attendance_id: int
    status: Literal["present", "absent"]
