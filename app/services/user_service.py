from sqlalchemy.orm import Session
from ..db.models.user import User

def get_students(db: Session, school_id: int):
    return db.query(User).filter(
        User.SchoolId == school_id,
        User.RoleId == 4
    ).all()