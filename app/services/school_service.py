from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models.school import School
from ..db.models.user import User
from ..core.security import hash_password, generate_temp_password, generate_password_reset_token
from ..utils.email_service import send_admin_onboarding_email


def create_school(db: Session, school_name: str, address: str, phone_number: str, email: str):
    # Check if school already exists
    existing_school = db.query(School).filter(School.Email == email).first()
    if existing_school:
        raise HTTPException(status_code=400, detail="School with this email already exists")

    # Check if school name is unique
    existing_by_name = db.query(School).filter(School.SchoolName == school_name).first()
    if existing_by_name:
        raise HTTPException(status_code=400, detail="School with this name already exists")

    # Create new school
    new_school = School(
        SchoolName=school_name,
        Address=address,
        PhoneNumber=phone_number,
        Email=email,
        IsActive=True
    )

    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    return {
        "school_id": new_school.SchoolId,
        "school_name": new_school.SchoolName,
        "address": new_school.Address,
        "phone_number": new_school.PhoneNumber,
        "email": new_school.Email,
        "is_active": new_school.IsActive,
        "created_at": new_school.CreatedAt
    }


def get_all_schools(db: Session):
    schools = db.query(School).all()
    
    if not schools:
        return []
    
    return [
        {
            "school_id": school.SchoolId,
            "school_name": school.SchoolName,
            "address": school.Address,
            "phone_number": school.PhoneNumber,
            "email": school.Email,
            "is_active": school.IsActive,
            "created_at": school.CreatedAt
        }
        for school in schools
    ]


def create_school_admin(
    db: Session,
    admin_name: str,
    admin_email: str,
    phone_number: str,
    school_id: int,
    created_by_user_id: int,
    reset_password_base_url: str
):
    """
    Create a school admin with temporary password and send onboarding email.
    
    Args:
        db: Database session
        admin_name: Name of the admin
        admin_email: Email of the admin
        phone_number: Phone number of the admin
        school_id: School ID to assign the admin to
        created_by_user_id: User ID of the super admin creating this admin
        reset_password_base_url: Base URL for password reset link (e.g., http://yourapp.com/reset-password)
    
    Returns:
        Admin user object
    """
    
    # Check if admin email already exists
    existing_admin = db.query(User).filter(User.Email == admin_email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")
    
    # Check if school exists
    school = db.query(School).filter(School.SchoolId == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Generate temporary password
    temp_password = generate_temp_password()
    hashed_temp_password = hash_password(temp_password)
    
    # Generate password reset token
    # Create user first to get the user ID, then generate token
    new_admin = User(
        UserName=admin_name,
        SchoolId=school_id,
        Email=admin_email,
        Password=hashed_temp_password,
        PhoneNumber=phone_number,
        RoleId=2,  # RoleId 2 is for School Admin
        IsPasswordUpdated=False,
        CreatedBy=created_by_user_id
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    # Generate password reset token with the new admin's ID
    reset_token = generate_password_reset_token(new_admin.UserId, admin_email)
    
    # Create reset password link
    reset_password_link = f"{reset_password_base_url}?token={reset_token}"
    
    # Send onboarding email
    email_sent = send_admin_onboarding_email(
        admin_email=admin_email,
        admin_name=admin_name,
        temp_password=temp_password,
        reset_password_link=reset_password_link
    )
    
    if not email_sent:
        # Log the error but don't fail the operation
        print(f"Warning: Email not sent to {admin_email}")
    
    return {
        "user_id": new_admin.UserId,
        "user_name": new_admin.UserName,
        "school_id": new_admin.SchoolId,
        "email": new_admin.Email,
        "phone_number": new_admin.PhoneNumber,
        "role_id": new_admin.RoleId,
        "is_password_updated": new_admin.IsPasswordUpdated,
        "created_at": new_admin.CreatedAt,
        "message": "Admin created successfully. Onboarding email has been sent."
    }
