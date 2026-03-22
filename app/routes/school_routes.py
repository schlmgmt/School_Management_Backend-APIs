from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.input.school_input import SchoolCreateRequest
from ..schemas.input.admin_input import CreateSchoolAdminRequest
from ..schemas.output.school_output import SchoolResponse
from ..schemas.output.admin_output import SchoolAdminResponse
from ..services.school_service import create_school, get_all_schools, create_school_admin
from ..core.dependencies import require_role

SUPER_ADMIN = 1

router = APIRouter(prefix="/schools", tags=["Schools"])


@router.post("/", response_model=SchoolResponse)
def add_school(
    data: SchoolCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([SUPER_ADMIN]))
):
    """
    Create a new school. Only Super Admin can perform this action.
    """
    return create_school(db, data.school_name, data.address, data.phone_number, data.email)


@router.get("/", response_model=List[SchoolResponse])
def list_all_schools(
    db: Session = Depends(get_db),
    user=Depends(require_role([SUPER_ADMIN]))
):
    """
    Get all schools. Only Super Admin can perform this action.
    """
    return get_all_schools(db)


@router.post("/{school_id}/admin", response_model=SchoolAdminResponse)
def add_school_admin(
    school_id: int,
    data: CreateSchoolAdminRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role([SUPER_ADMIN]))
):
    """
    Create a new school admin. Only Super Admin can perform this action.
    
    Flow:
    - Super admin provides admin details
    - System generates temporary password
    - Onboarding email sent with password reset link
    - Admin must click link and reset password to set IsPasswordUpdated = true
    """
    reset_password_base_url = "http://yourapp.com/reset-password"  # Update with your actual frontend URL
    
    return create_school_admin(
        db=db,
        admin_name=data.admin_name,
        admin_email=data.admin_email,
        phone_number=data.phone_number,
        school_id=data.school_id,
        created_by_user_id=user.get("user_id"),
        reset_password_base_url=reset_password_base_url
    )
