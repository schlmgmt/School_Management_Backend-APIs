from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..db.database import get_db
from ..core.dependencies import get_current_user
from ..services.attendance_service import AttendanceService
from ..schemas.input.attendance_input import AttendanceMarkRequest, AttendanceUpdateRequest
from ..schemas.output.attendance_output import AttendanceResponse, BulkAttendanceResponse

router = APIRouter(prefix="/api/v1/attendance", tags=["Attendance"])

ADMIN = 2
TEACHER = 3
STUDENT = 4


@router.post("", response_model=BulkAttendanceResponse)
def mark_attendance(
    request: AttendanceMarkRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Mark attendance for multiple students in a class/section. Only class teacher can mark attendance.
    Class teacher is determined from the Section model.
    
    Request:
    {
      "class_id": 1,
      "section_id": 2,
      "date": "2026-03-25",
      "students": [
        { "student_id": 1, "status": "present" },
        { "student_id": 2, "status": "absent" }
      ]
    }
    """
    # Only teachers can mark attendance
    if current_user["role"] != TEACHER:
        raise HTTPException(
            status_code=403,
            detail="Only teachers can mark attendance"
        )
    
    from ..db.models.teacher import Teacher
    
    # Get teacher ID from user
    teacher = db.query(Teacher).filter(Teacher.UserId == current_user["user_id"]).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    result = AttendanceService.mark_attendance(
        db=db,
        class_id=request.class_id,
        section_id=request.section_id,
        date_obj=request.date,
        students=request.students,
        teacher_id=teacher.TeacherId,
        school_id=current_user["school_id"]
    )
    
    # If no records were created, raise an error
    if not result["attendance_records"]:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to mark attendance for all students. Errors: {result['errors']}"
        )
    
    return {
        "class_id": request.class_id,
        "section_id": request.section_id,
        "date": request.date,
        "total_marked": result["success_count"],
        "attendance_records": result["attendance_records"]
    }


@router.get("", response_model=List[AttendanceResponse])
def get_attendance(
    class_id: int = Query(..., description="Class ID"),
    section_id: int = Query(..., description="Section ID"),
    date: date = Query(..., description="Date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get attendance for a class and section on a specific date.
    Teacher must be assigned to teach this class-section.
    """
    if current_user["role"] != TEACHER:
        raise HTTPException(
            status_code=403,
            detail="Only teachers can view attendance"
        )
    
    from ..db.models.teacher import Teacher
    
    # Get teacher ID from user
    teacher = db.query(Teacher).filter(Teacher.UserId == current_user["user_id"]).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    attendance_records = AttendanceService.get_attendance_by_class_date(
        db=db,
        class_id=class_id,
        section_id=section_id,
        date_obj=date,
        teacher_id=teacher.TeacherId,
        school_id=current_user["school_id"]
    )
    
    return attendance_records


@router.get("/student/{student_id}", response_model=List[AttendanceResponse])
def get_student_attendance_history(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get attendance history for a student.
    Teachers can view attendance for students in their assigned classes.
    """
    if current_user["role"] not in [TEACHER, ADMIN]:
        raise HTTPException(
            status_code=403,
            detail="Only teachers and admins can view student attendance history"
        )
    
    attendance_records = AttendanceService.get_student_attendance_history(
        db=db,
        student_id=student_id,
        school_id=current_user["school_id"]
    )
    
    return attendance_records


@router.put("", response_model=AttendanceResponse)
def update_attendance(
    request: AttendanceUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update attendance status. Only class teacher can update.
    
    Request:
    {
      "attendance_id": 1,
      "status": "absent"
    }
    """
    if current_user["role"] != TEACHER:
        raise HTTPException(
            status_code=403,
            detail="Only teachers can update attendance"
        )
    
    from ..db.models.teacher import Teacher
    
    # Get teacher ID from user
    teacher = db.query(Teacher).filter(Teacher.UserId == current_user["user_id"]).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    attendance = AttendanceService.update_attendance(
        db=db,
        attendance_id=request.attendance_id,
        status=request.status,
        teacher_id=teacher.TeacherId,
        school_id=current_user["school_id"]
    )
    
    return attendance
