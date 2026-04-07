from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.user_service import get_students, get_user_by_id, can_view_user
from ..schemas.output.user_output import UserResponse
from ..core.dependencies import require_role, get_current_user

ADMIN = 2
TEACHER = 3

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/students")
def students(
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN, TEACHER]))
):
    return get_students(db, user["school_id"])

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_data = get_user_by_id(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not can_view_user(user, user_data):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return user_data