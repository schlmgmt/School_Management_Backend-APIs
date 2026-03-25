from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..db.models.teacher import Teacher
from ..db.models.user import User
from ..core.security import hash_password, generate_temp_password, generate_password_reset_token
from ..utils.email_service import send_admin_onboarding_email


def create_teacher_with_user(
    db: Session,
    teacher_name: str,
    email: str,
    school_id: int,
    phone_number: str,
    subject: str,
    qualification: str,
    experience_years: int,
    sec_phone_number: str = None,
    date_of_birth = None,
    joining_date = None,
    reset_password_base_url: str = None
):
    """
    Create a new teacher with user account and send password reset email.
    
    Step 1: Create User record
    Step 2: Create Teacher record
    Step 3: Send password reset email
    
    Args:
        db: Database session
        teacher_name: Teacher's name (will be used as username)
        email: Teacher's email (unique in user table)
        school_id: School ID (from admin's school)
        phone_number: Teacher phone number
        subject: Subject taught
        qualification: Teacher qualification
        experience_years: Years of experience
        sec_phone_number: Secondary phone number (optional)
        date_of_birth: Date of birth
        joining_date: Joining date
        reset_password_base_url: Base URL for password reset link
    
    Returns:
        Dictionary with teacher and user creation info
    """
    
    TEACHER_ROLE_ID = 3
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.Email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered in the system")
    
    existing_teacher = db.query(Teacher).filter(Teacher.Email == email).first()
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher with this email already exists")
    
    # Step 1: Create User
    try:
        temp_password = generate_temp_password()
        hashed_password = hash_password(temp_password)
        
        new_user = User(
            UserName=teacher_name,
            Email=email,
            Password=hashed_password,
            PhoneNumber=phone_number,
            SchoolId=school_id,
            RoleId=TEACHER_ROLE_ID,
            IsPasswordUpdated=False,
            CreatedAt=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        user_id = new_user.UserId
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")
    
    # Step 2: Create Teacher
    try:
        new_teacher = Teacher(
            UserId=user_id,
            Email=email,
            Subject=subject,
            Qualification=qualification,
            ExperienceYears=experience_years,
            PhoneNumber=phone_number,
            SecPhoneNumber=sec_phone_number,
            DateOfBirth=date_of_birth,
            JoiningDate=joining_date,
            IsActive=True
        )
        
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create teacher record: {str(e)}")
    
    # Step 3: Send password reset email
    if reset_password_base_url:
        try:
            reset_token = generate_password_reset_token(user_id, email)
            reset_password_link = f"{reset_password_base_url}?token={reset_token}"
            
            email_sent = send_admin_onboarding_email(
                admin_email=email,
                admin_name=teacher_name,
                temp_password=temp_password,
                reset_password_link=reset_password_link
            )
            
            if not email_sent:
                print(f"Warning: Email not sent to {email}")
        except Exception as e:
            print(f"Warning: Failed to send email to {email}: {str(e)}")
    
    return {
        "teacher_id": new_teacher.TeacherId,
        "user_id": user_id,
        "email": email,
        "teacher_name": teacher_name,
        "is_active": new_teacher.IsActive,
        "created_at": new_teacher.CreatedAt,
        "message": "Teacher account created successfully. Password reset email has been sent."
    }


def get_teacher_by_id(db: Session, teacher_id: int, school_id: int = None):
    """
    Get teacher by ID. Optional school_id for school-scoped queries.
    
    Args:
        db: Database session
        teacher_id: Teacher ID to fetch
        school_id: School ID (optional, for validation)
    
    Returns:
        Teacher object dict or raises HTTPException if not found
    """
    
    teacher = db.query(Teacher).filter(Teacher.TeacherId == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # If school_id provided, verify teacher belongs to that school
    if school_id:
        user = db.query(User).filter(User.UserId == teacher.UserId, User.SchoolId == school_id).first()
        if not user:
            raise HTTPException(status_code=403, detail="Teacher does not belong to your school")
    
    return format_teacher_response(teacher)


def get_all_teachers_in_school(db: Session, school_id: int):
    """
    Get all teachers in a school. Everyone can view (no role restriction).
    
    Args:
        db: Database session
        school_id: School ID
    
    Returns:
        List of teacher objects
    """
    
    teachers = db.query(Teacher).join(User).filter(User.SchoolId == school_id).all()
    
    if not teachers:
        return []
    
    return [format_teacher_response(teacher) for teacher in teachers]


def get_teacher_by_user_id(db: Session, user_id: int):
    """
    Get teacher record by User ID.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        Teacher object dict or raises HTTPException if not found
    """
    
    teacher = db.query(Teacher).filter(Teacher.UserId == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher record not found")
    
    return format_teacher_response(teacher)


def update_teacher(
    db: Session,
    teacher_id: int,
    school_id: int,
    subject: str = None,
    qualification: str = None,
    experience_years: int = None,
    phone_number: str = None,
    sec_phone_number: str = None,
    date_of_birth = None,
    joining_date = None
):
    """
    Update teacher details. Only Admin can update.
    
    Args:
        db: Database session
        teacher_id: Teacher ID to update
        school_id: School ID (for validation)
        All other parameters are optional
    
    Returns:
        Updated teacher object dict
    """
    
    teacher = db.query(Teacher).filter(Teacher.TeacherId == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Verify teacher belongs to the school
    user = db.query(User).filter(User.UserId == teacher.UserId, User.SchoolId == school_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Teacher does not belong to your school")
    
    # Update fields
    if subject is not None:
        teacher.Subject = subject
    
    if qualification is not None:
        teacher.Qualification = qualification
    
    if experience_years is not None:
        teacher.ExperienceYears = experience_years
    
    if phone_number is not None:
        teacher.PhoneNumber = phone_number
    
    if sec_phone_number is not None:
        teacher.SecPhoneNumber = sec_phone_number
    
    if date_of_birth is not None:
        teacher.DateOfBirth = date_of_birth
    
    if joining_date is not None:
        teacher.JoiningDate = joining_date
    
    teacher.UpdatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(teacher)
    
    return format_teacher_response(teacher)


def toggle_teacher_status(db: Session, teacher_id: int, school_id: int, is_active: bool):
    """
    Enable or disable a teacher. Only Admin can modify.
    
    Args:
        db: Database session
        teacher_id: Teacher ID to update
        school_id: School ID (for validation)
        is_active: Boolean value for active status
    
    Returns:
        Updated teacher object dict
    """
    
    teacher = db.query(Teacher).filter(Teacher.TeacherId == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Verify teacher belongs to the school
    user = db.query(User).filter(User.UserId == teacher.UserId, User.SchoolId == school_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Teacher does not belong to your school")
    
    teacher.IsActive = is_active
    teacher.UpdatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(teacher)
    
    return format_teacher_response(teacher)


def format_teacher_response(teacher):
    """
    Format teacher database object to response dict.
    """
    return {
        "teacher_id": teacher.TeacherId,
        "user_id": teacher.UserId,
        "email": teacher.Email,
        "subject": teacher.Subject,
        "qualification": teacher.Qualification,
        "experience_years": teacher.ExperienceYears,
        "phone_number": teacher.PhoneNumber,
        "sec_phone_number": teacher.SecPhoneNumber,
        "date_of_birth": teacher.DateOfBirth,
        "joining_date": teacher.JoiningDate,
        "is_active": teacher.IsActive,
        "created_at": teacher.CreatedAt,
        "updated_at": teacher.UpdatedAt
    }
