from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..core.dependencies import get_current_user
from ..services.teacher_class_mapping_service import TeacherClassMappingService
from ..schemas.input.teacher_class_mapping_input import TeacherClassMappingCreateRequest
from ..schemas.output.teacher_class_mapping_output import TeacherClassMappingResponse

router = APIRouter(prefix="/api/v1/teacher-class-mapping", tags=["Teacher Class Mapping"])

ADMIN = 2
TEACHER = 3


@router.post("", response_model=TeacherClassMappingResponse)
def assign_class_to_teacher(
    request: TeacherClassMappingCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Assign a class and section to a teacher. Only Admin can do this.
    """
    # Only Admin can assign classes to teachers
    if current_user["role"] != ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can assign classes to teachers"
        )
    
    mapping = TeacherClassMappingService.create_mapping(
        db=db,
        teacher_id=request.teacher_id,
        class_id=request.class_id,
        section_id=request.section_id,
        subject=request.subject,
        school_id=current_user["school_id"]
    )
    
    return mapping


@router.get("", response_model=List[TeacherClassMappingResponse])
def get_assigned_classes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get assigned classes for current user.
    - Teachers see their own assigned classes
    - Admins see all teacher assignments in their school
    """
    if current_user["role"] == TEACHER:
        # Get teacher's profile to get TeacherId
        from ..db.models.teacher import Teacher
        teacher = db.query(Teacher).filter(Teacher.UserId == current_user["user_id"]).first()
        
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher profile not found")
        
        mappings = TeacherClassMappingService.get_mappings_by_teacher(db, teacher.TeacherId)
        return mappings
    
    elif current_user["role"] == ADMIN:
        # Admin sees all assignments in their school
        mappings = TeacherClassMappingService.get_all_mappings_by_school(db, current_user["school_id"])
        return mappings
    
    else:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view class assignments"
        )


@router.delete("/{mapping_id}")
def delete_class_assignment(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a class assignment. Only Admin can do this.
    """
    # Only Admin can delete assignments
    if current_user["role"] != ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can delete class assignments"
        )
    
    result = TeacherClassMappingService.delete_mapping(db, mapping_id)
    return result
