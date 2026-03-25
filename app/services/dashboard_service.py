from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models.user import User
from ..db.models.school import School


def get_dashboard_stats(db: Session, user_role: int, user_school_id: int = None):
    """
    Get dashboard statistics.
    
    Args:
        db: Database session
        user_role: Role ID of the logged-in user (1=SuperAdmin, 2=Admin, etc.)
        user_school_id: SchoolId of the logged-in user (required for non-super-admin)
    
    Returns:
        Dictionary with dashboard statistics
    """
    
    SUPER_ADMIN = 1
    ADMIN = 2
    TEACHER = 3
    STUDENT = 4
    
    if user_role == SUPER_ADMIN:
        # Super Admin: Get overall statistics for all schools
        
        # Total schools
        total_schools = db.query(School).count()
        
        # Active schools
        active_schools = db.query(School).filter(School.IsActive == True).count()
        
        # Total admins (RoleId = 2)
        total_admins = db.query(User).filter(User.RoleId == ADMIN).count()
        
        # Total students (RoleId = 4)
        total_students = db.query(User).filter(User.RoleId == STUDENT).count()
        
        # Total teachers (RoleId = 3)
        total_teachers = db.query(User).filter(User.RoleId == TEACHER).count()
        
    else:
        # Non-Super Admin: Get statistics for their school only
        
        if not user_school_id:
            raise HTTPException(status_code=400, detail="School ID is required for non-admin users")
        
        # Check if school exists
        school = db.query(School).filter(School.SchoolId == user_school_id).first()
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        # Total schools (1 for their school)
        total_schools = 1
        
        # Active schools (check if their school is active)
        active_schools = 1 if school.IsActive else 0
        
        # Total admins in this school (RoleId = 2 and SchoolId matches)
        total_admins = db.query(User).filter(
            User.RoleId == ADMIN,
            User.SchoolId == user_school_id
        ).count()
        
        # Total students in this school (RoleId = 4 and SchoolId matches)
        total_students = db.query(User).filter(
            User.RoleId == STUDENT,
            User.SchoolId == user_school_id
        ).count()
        
        # Total teachers in this school (RoleId = 3 and SchoolId matches)
        total_teachers = db.query(User).filter(
            User.RoleId == TEACHER,
            User.SchoolId == user_school_id
        ).count()
    
    return {
        "total_schools": total_schools,
        "active_schools": active_schools,
        "total_admins": total_admins,
        "total_students": total_students,
        "total_teachers": total_teachers
    }
