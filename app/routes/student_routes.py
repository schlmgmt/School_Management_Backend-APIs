from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.input.student_input import StudentCreateRequest, StudentUpdateRequest, StudentStatusRequest
from ..schemas.output.student_output import StudentResponse
from ..services.student_service import (
    create_student_with_user,
    get_student_by_id,
    get_all_students_in_school,
    get_student_by_user_id,
    update_student,
    toggle_student_status
)
from ..core.dependencies import require_role, get_current_user

ADMIN = 2
STUDENT = 4

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=dict)
def create_new_student(
    data: StudentCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Create a new student account with User and Student records.
    Only Admin can perform this action.
    
    This endpoint:
    Step 1: Creates a User record with temporary password
    Step 2: Creates a Student record linked to the user
    Step 3: Sends password reset email to the student
    
    Parameters:
    - student_name: Student's name (username)
    - email: Student's email (must be unique)
    - class_id: Class ID
    - section_id: Section ID
    - roll_number: Student roll number
    - fathers_name: Father's name
    - mothers_name: Mother's name
    - phone_number: Student phone number
    - sec_phone_number: Secondary phone number (optional)
    - date_of_birth: Date of birth (format: YYYY-MM-DD)
    - admission_date: Admission date (format: YYYY-MM-DD)
    
    Response:
    Returns student creation details including student_id, user_id, and confirmation message
    """
    admin_school_id = user.get("school_id")
    reset_password_base_url = "http://yourapp.com/reset-password"  # Update with your actual frontend URL
    
    return create_student_with_user(
        db=db,
        student_name=data.student_name,
        email=data.email,
        school_id=admin_school_id,
        phone_number=data.phone_number,
        class_id=data.class_id,
        section_id=data.section_id,
        roll_number=data.roll_number,
        fathers_name=data.fathers_name,
        mothers_name=data.mothers_name,
        sec_phone_number=data.sec_phone_number,
        date_of_birth=data.date_of_birth,
        admission_date=data.admission_date,
        reset_password_base_url=reset_password_base_url
    )


@router.get("/", response_model=List[StudentResponse])
def list_all_students(
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Get all students in the admin's school. Only Admin can perform this action.
    
    Returns a list of all students in the school.
    """
    school_id = user.get("school_id")
    
    return get_all_students_in_school(db=db, school_id=school_id)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Get student details by ID.
    
    Authorization:
    - Admin: Can view any student in their school
    - Student: Can only view their own student record
    """
    user_role = user.get("role")
    user_id = user.get("user_id")
    school_id = user.get("school_id")
    
    if user_role == ADMIN:
        # Admin can view any student in their school
        return get_student_by_id(db=db, student_id=student_id, school_id=school_id)
    
    elif user_role == STUDENT:
        # Student can only view their own record
        student = get_student_by_id(db=db, student_id=student_id)
        
        # Verify this student record belongs to the current user
        if student["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own student record"
            )
        
        return student
    
    else:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view student records"
        )


@router.get("/me/profile", response_model=StudentResponse)
def get_my_student_profile(
    db: Session = Depends(get_db),
    user=Depends(require_role([STUDENT]))
):
    """
    Get logged-in student's own profile. Only accessible by Student role.
    """
    user_id = user.get("user_id")
    
    return get_student_by_user_id(db=db, user_id=user_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student_details(
    student_id: int,
    data: StudentUpdateRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Update student details. Only Admin can perform this action.
    
    Parameters:
    - student_id: Student ID to update
    - data: Student update data (all fields optional)
    """
    school_id = user.get("school_id")
    
    return update_student(
        db=db,
        student_id=student_id,
        school_id=school_id,
        class_id=data.class_id,
        section_id=data.section_id,
        roll_number=data.roll_number,
        fathers_name=data.fathers_name,
        mothers_name=data.mothers_name,
        phone_number=data.phone_number,
        sec_phone_number=data.sec_phone_number,
        date_of_birth=data.date_of_birth,
        admission_date=data.admission_date
    )


@router.patch("/{student_id}/status", response_model=StudentResponse)
def change_student_status(
    student_id: int,
    data: StudentStatusRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Enable or disable a student. Only Admin can perform this action.
    
    Parameters:
    - student_id: Student ID to update
    - data: Contains is_active boolean (true to enable, false to disable)
    """
    school_id = user.get("school_id")
    
    return toggle_student_status(
        db=db,
        student_id=student_id,
        school_id=school_id,
        is_active=data.is_active
    )
