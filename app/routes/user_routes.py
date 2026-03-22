from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.user_service import get_students
from ..core.dependencies import require_role

ADMIN = 2
TEACHER = 3

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/students")
def students(
    db: Session = Depends(get_db),
    user=Depends(require_role([ADMIN, TEACHER]))
):
    return get_students(db, user["school_id"])