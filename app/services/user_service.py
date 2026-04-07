from sqlalchemy.orm import Session
from ..db.models.user import User
from fastapi import HTTPException

SUPER_ADMIN = 1
ADMIN = 2
TEACHER = 3
STUDENT = 4

def get_students(db: Session, school_id: int):
    return db.query(User).filter(
        User.SchoolId == school_id,
        User.RoleId == 4
    ).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.UserId == user_id).first()

def can_view_user(current_user: dict, target_user: User) -> bool:
    """
    Check if current user has permission to view target user's profile
    - Super admin (role 1): can view anyone
    - Admin (role 2): can view teachers and students within their school
    - Teacher (role 3): can view students from their school and class
    - Student (role 4): can view their own profile only
    """
    current_role = current_user.get("role")
    current_user_id = current_user.get("user_id")
    current_school_id = current_user.get("school_id")
    current_class_id = current_user.get("class_id")
    
    # Super admin can view anyone
    if current_role == SUPER_ADMIN:
        return True
    
    # User can view their own profile
    if current_user_id == target_user.UserId:
        return True
    
    # Admin can view teachers and students within their school
    if current_role == ADMIN:
        if target_user.RoleId in [TEACHER, STUDENT] and target_user.SchoolId == current_school_id:
            return True
    
    # Teacher can view students from their school and class
    if current_role == TEACHER:
        if target_user.RoleId == STUDENT and target_user.SchoolId == current_school_id and target_user.ClassId == current_class_id:
            return True
    
    return False