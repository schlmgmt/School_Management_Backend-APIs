from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.output.dashboard_output import DashboardResponse
from ..services.dashboard_service import get_dashboard_stats
from ..core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Get dashboard statistics.
    
    Authorization:
    - Super Admin: Returns overall statistics for all schools
    - Other roles: Returns statistics for their school only
    
    Returns:
    - total_schools: Total number of schools
    - active_schools: Number of active schools
    - total_admins: Total number of admins
    - total_students: Total number of students
    - total_teachers: Total number of teachers
    """
    user_role = user.get("role")
    user_school_id = user.get("school_id")
    
    return get_dashboard_stats(
        db=db,
        user_role=user_role,
        user_school_id=user_school_id
    )
