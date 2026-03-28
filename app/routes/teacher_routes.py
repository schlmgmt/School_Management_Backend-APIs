from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.input.teacher_input import TeacherCreateRequest, TeacherUpdateRequest, TeacherStatusRequest
from ..schemas.output.teacher_output import TeacherResponse
from ..services.teacher_service import (
    create_teacher_with_user,
    get_teacher_by_id,
    get_all_teachers_in_school,
    get_teacher_by_user_id,
    update_teacher,
    toggle_teacher_status
)
from ..services.student_service import get_students_by_class_and_section
from ..services.teacher_class_mapping_service import TeacherClassMappingService
from ..core.dependencies import require_role, get_current_user

ADMIN = 2
TEACHER = 3

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("/", response_model=dict)
def create_new_teacher(
    data: TeacherCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Create a new teacher account with User and Teacher records.
    Only Admin can perform this action.
    
    This endpoint:
    Step 1: Creates a User record with temporary password
    Step 2: Creates a Teacher record linked to the user
    Step 3: Sends password reset email to the teacher
    
    Parameters:
    - teacher_name: Teacher's name (username)
    - email: Teacher's email (must be unique)
    - subject: Subject taught
    - qualification: Teacher qualification
    - experience_years: Years of experience
    - phone_number: Teacher phone number
    - sec_phone_number: Secondary phone number (optional)
    - date_of_birth: Date of birth (format: YYYY-MM-DD)
    - joining_date: Joining date (format: YYYY-MM-DD)
    
    Response:
    Returns teacher creation details including teacher_id, user_id, and confirmation message
    """
    admin_school_id = user.get("school_id")
    reset_password_base_url = "exp://localhost/reset-password"  # Update with your actual frontend URL
    
    return create_teacher_with_user(
        db=db,
        teacher_name=data.teacher_name,
        email=data.email,
        school_id=admin_school_id,
        phone_number=data.phone_number,
        subject=data.subject,
        qualification=data.qualification,
        experience_years=data.experience_years,
        sec_phone_number=data.sec_phone_number,
        date_of_birth=data.date_of_birth,
        joining_date=data.joining_date,
        reset_password_base_url=reset_password_base_url
    )


@router.get("/", response_model=List[TeacherResponse])
def list_all_teachers(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Get all teachers in the user's school. Everyone (all authenticated users) can view.
    """
    school_id = user.get("school_id")
    
    return get_all_teachers_in_school(db=db, school_id=school_id)


@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Get teacher details by ID.
    
    Authorization:
    - Everyone (all authenticated users) can view teacher details
    """
    school_id = user.get("school_id")
    
    return get_teacher_by_id(db=db, teacher_id=teacher_id, school_id=school_id)


@router.get("/me/profile", response_model=TeacherResponse)
def get_my_teacher_profile(
    db: Session = Depends(get_db),
    user=Depends(require_role([TEACHER]))
):
    """
    Get logged-in teacher's own profile. Only accessible by Teacher role.
    """
    user_id = user.get("user_id")
    
    return get_teacher_by_user_id(db=db, user_id=user_id)


@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher_details(
    teacher_id: int,
    data: TeacherUpdateRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Update teacher details. Only Admin can perform this action.
    
    Parameters:
    - teacher_id: Teacher ID to update
    - data: Teacher update data (all fields optional)
    """
    school_id = user.get("school_id")
    
    return update_teacher(
        db=db,
        teacher_id=teacher_id,
        school_id=school_id,
        subject=data.subject,
        qualification=data.qualification,
        experience_years=data.experience_years,
        phone_number=data.phone_number,
        sec_phone_number=data.sec_phone_number,
        date_of_birth=data.date_of_birth,
        joining_date=data.joining_date
    )


@router.patch("/{teacher_id}/status", response_model=TeacherResponse)
def change_teacher_status(
    teacher_id: int,
    data: TeacherStatusRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN]))
):
    """
    Enable or disable a teacher. Only Admin can perform this action.
    
    Parameters:
    - teacher_id: Teacher ID to update
    - data: Contains is_active boolean (true to enable, false to disable)
    """
    school_id = user.get("school_id")
    
    return toggle_teacher_status(
        db=db,
        teacher_id=teacher_id,
        school_id=school_id,
        is_active=data.is_active
    )


@router.get("/me/students", response_model=List[dict])
def get_my_students(
    db: Session = Depends(get_db),
    user=Depends(require_role([TEACHER]))
):
    """
    Get all students from classes and sections assigned to the logged-in teacher.
    Only accessible by Teacher role.
    
    Returns a list of all students the teacher is assigned to teach.
    """
    from ..db.models.teacher import Teacher
    
    user_id = user.get("user_id")
    school_id = user.get("school_id")
    
    # Get teacher's profile
    teacher = db.query(Teacher).filter(Teacher.UserId == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get all class-section assignments for this teacher
    mappings = TeacherClassMappingService.get_mappings_by_teacher(db, teacher.TeacherId)
    
    if not mappings:
        return []
    
    # Collect all students from all assigned classes/sections
    all_students = []
    for mapping in mappings:
        students = get_students_by_class_and_section(
            db=db,
            class_id=mapping.ClassId,
            section_id=mapping.SectionId,
            school_id=school_id
        )
        all_students.extend(students)
    
    return all_students


@router.get("/me/students/class/{class_id}/section/{section_id}", response_model=List[dict])
def get_students_in_my_class_section(
    class_id: int,
    section_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role([TEACHER]))
):
    """
    Get students from a specific class and section assigned to the logged-in teacher.
    Only accessible by Teacher role.
    
    Parameters:
    - class_id: Class ID
    - section_id: Section ID
    
    Returns a list of students in the specified class and section that teacher is assigned to.
    """
    from ..db.models.teacher import Teacher
    from ..db.models.teacher_class_mapping import TeacherClassMapping
    
    user_id = user.get("user_id")
    school_id = user.get("school_id")
    
    # Get teacher's profile
    teacher = db.query(Teacher).filter(Teacher.UserId == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Verify teacher is assigned to this class-section
    mapping = db.query(TeacherClassMapping).filter(
        TeacherClassMapping.TeacherId == teacher.TeacherId,
        TeacherClassMapping.ClassId == class_id,
        TeacherClassMapping.SectionId == section_id
    ).first()
    
    if not mapping:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to teach this class and section"
        )
    
    # Get students in this class/section
    students = get_students_by_class_and_section(
        db=db,
        class_id=class_id,
        section_id=section_id,
        school_id=school_id
    )
    
    return students
