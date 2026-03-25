from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..db.models.student import Student
from ..db.models.user import User
from ..core.security import hash_password, generate_temp_password, generate_password_reset_token
from ..utils.email_service import send_admin_onboarding_email


def create_student_with_user(
    db: Session,
    student_name: str,
    email: str,
    school_id: int,
    phone_number: str,
    class_id: int,
    section_id: int,
    roll_number: str,
    fathers_name: str,
    mothers_name: str,
    sec_phone_number: str = None,
    date_of_birth = None,
    admission_date = None,
    reset_password_base_url: str = None
):
    """
    Create a new student with user account and send password reset email.
    
    Step 1: Create User record
    Step 2: Create Student record
    Step 3: Send password reset email
    
    Args:
        db: Database session
        student_name: Student's name (will be used as username)
        email: Student's email (unique in user table)
        school_id: School ID (from admin's school)
        phone_number: Student phone number
        class_id: Class ID
        section_id: Section ID
        roll_number: Student roll number
        fathers_name: Father's name
        mothers_name: Mother's name
        sec_phone_number: Secondary phone number (optional)
        date_of_birth: Date of birth
        admission_date: Admission date
        reset_password_base_url: Base URL for password reset link
    
    Returns:
        Dictionary with student and user creation info
    """
    
    STUDENT_ROLE_ID = 4
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.Email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered in the system")
    
    existing_student = db.query(Student).filter(Student.Email == email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this email already exists")
    
    # Step 1: Create User
    try:
        temp_password = generate_temp_password()
        hashed_password = hash_password(temp_password)
        
        new_user = User(
            UserName=student_name,
            Email=email,
            Password=hashed_password,
            PhoneNumber=phone_number,
            SchoolId=school_id,
            RoleId=STUDENT_ROLE_ID,
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
    
    # Step 2: Create Student
    try:
        new_student = Student(
            UserId=user_id,
            Email=email,
            ClassId=class_id,
            SectionId=section_id,
            RollNumber=roll_number,
            FathersName=fathers_name,
            MothersName=mothers_name,
            PhoneNumber=phone_number,
            SecPhoneNumber=sec_phone_number,
            DateOfBirth=date_of_birth,
            AdmissionDate=admission_date,
            IsActive=True
        )
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create student record: {str(e)}")
    
    # Step 3: Send password reset email
    if reset_password_base_url:
        try:
            reset_token = generate_password_reset_token(user_id, email)
            reset_password_link = f"{reset_password_base_url}?token={reset_token}"
            
            email_sent = send_admin_onboarding_email(
                admin_email=email,
                admin_name=student_name,
                temp_password=temp_password,
                reset_password_link=reset_password_link
            )
            
            if not email_sent:
                print(f"Warning: Email not sent to {email}")
        except Exception as e:
            print(f"Warning: Failed to send email to {email}: {str(e)}")
    
    return {
        "student_id": new_student.StudentId,
        "user_id": user_id,
        "email": email,
        "student_name": student_name,
        "is_active": new_student.IsActive,
        "created_at": new_student.CreatedAt,
        "message": "Student account created successfully. Password reset email has been sent."
    }


def get_student_by_id(db: Session, student_id: int, school_id: int = None):
    """
    Get student by ID. Optional school_id for school-scoped queries.
    
    Args:
        db: Database session
        student_id: Student ID to fetch
        school_id: School ID (optional, for validation)
    
    Returns:
        Student object dict or raises HTTPException if not found
    """
    
    student = db.query(Student).filter(Student.StudentId == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # If school_id provided, verify student belongs to that school
    if school_id:
        user = db.query(User).filter(User.UserId == student.UserId, User.SchoolId == school_id).first()
        if not user:
            raise HTTPException(status_code=403, detail="Student does not belong to your school")
    
    return format_student_response(student)


def get_all_students_in_school(db: Session, school_id: int):
    """
    Get all students in a school.
    
    Args:
        db: Database session
        school_id: School ID
    
    Returns:
        List of student objects
    """
    
    students = db.query(Student).join(User).filter(User.SchoolId == school_id).all()
    
    if not students:
        return []
    
    return [format_student_response(student) for student in students]


def get_student_by_user_id(db: Session, user_id: int):
    """
    Get student record by User ID.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        Student object dict or raises HTTPException if not found
    """
    
    student = db.query(Student).filter(Student.UserId == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")
    
    return format_student_response(student)


def update_student(
    db: Session,
    student_id: int,
    school_id: int,
    class_id: int = None,
    section_id: int = None,
    roll_number: str = None,
    fathers_name: str = None,
    mothers_name: str = None,
    phone_number: str = None,
    sec_phone_number: str = None,
    date_of_birth = None,
    admission_date = None
):
    """
    Update student details.
    
    Args:
        db: Database session
        student_id: Student ID to update
        school_id: School ID (for validation)
        All other parameters are optional
    
    Returns:
        Updated student object dict
    """
    
    student = db.query(Student).filter(Student.StudentId == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify student belongs to the school
    user = db.query(User).filter(User.UserId == student.UserId, User.SchoolId == school_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Student does not belong to your school")
    
    # Update fields
    if class_id is not None:
        student.ClassId = class_id
    
    if section_id is not None:
        student.SectionId = section_id
    
    if roll_number is not None:
        student.RollNumber = roll_number
    
    if fathers_name is not None:
        student.FathersName = fathers_name
    
    if mothers_name is not None:
        student.MothersName = mothers_name
    
    if phone_number is not None:
        student.PhoneNumber = phone_number
    
    if sec_phone_number is not None:
        student.SecPhoneNumber = sec_phone_number
    
    if date_of_birth is not None:
        student.DateOfBirth = date_of_birth
    
    if admission_date is not None:
        student.AdmissionDate = admission_date
    
    student.UpdatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(student)
    
    return format_student_response(student)


def toggle_student_status(db: Session, student_id: int, school_id: int, is_active: bool):
    """
    Enable or disable a student.
    
    Args:
        db: Database session
        student_id: Student ID to update
        school_id: School ID (for validation)
        is_active: Boolean value for active status
    
    Returns:
        Updated student object dict
    """
    
    student = db.query(Student).filter(Student.StudentId == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify student belongs to the school
    user = db.query(User).filter(User.UserId == student.UserId, User.SchoolId == school_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Student does not belong to your school")
    
    student.IsActive = is_active
    student.UpdatedAt = datetime.utcnow()
    
    db.commit()
    db.refresh(student)
    
    return format_student_response(student)


def get_students_by_class_and_section(db: Session, class_id: int, section_id: int, school_id: int = None):
    """
    Get all students in a specific class and section.
    Optionally verify they belong to a specific school.
    
    Args:
        db: Database session
        class_id: Class ID
        section_id: Section ID
        school_id: School ID (optional, for validation)
    
    Returns:
        List of student objects
    """
    query = db.query(Student).filter(
        Student.ClassId == class_id,
        Student.SectionId == section_id
    )
    
    # If school_id provided, verify students belong to that school
    if school_id:
        query = query.join(User).filter(User.SchoolId == school_id)
    
    students = query.all()
    
    if not students:
        return []
    
    return [format_student_response(student) for student in students]


def format_student_response(student):
    """
    Format student database object to response dict.
    """
    return {
        "student_id": student.StudentId,
        "user_id": student.UserId,
        "email": student.Email,
        "class_id": student.ClassId,
        "section_id": student.SectionId,
        "roll_number": student.RollNumber,
        "fathers_name": student.FathersName,
        "mothers_name": student.MothersName,
        "phone_number": student.PhoneNumber,
        "sec_phone_number": student.SecPhoneNumber,
        "date_of_birth": student.DateOfBirth,
        "admission_date": student.AdmissionDate,
        "is_active": student.IsActive,
        "created_at": student.CreatedAt,
        "updated_at": student.UpdatedAt
    }
