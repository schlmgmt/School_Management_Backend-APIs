from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..core.dependencies import get_current_user
from ..services.class_service import ClassService, SectionService
from ..schemas.input.class_input import (
    ClassCreateRequest, ClassUpdateRequest, ClassStatusRequest,
    SectionCreateRequest, SectionUpdateRequest, SectionStatusRequest
)
from ..schemas.output.class_output import ClassResponse, SectionResponse
from typing import List

router = APIRouter(prefix="/api/v1", tags=["Class & Section"])


# ============= CLASS ENDPOINTS =============

@router.post("/classes", response_model=ClassResponse)
def create_class(
    request: ClassCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new class. Only Admin (RoleId=2) can create classes.
    """
    # Only Admin can create classes
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can create classes"
        )
    
    class_obj = ClassService.create_class(
        db=db,
        school_id=current_user["school_id"],
        class_name=request.class_name
    )
    
    return class_obj


@router.get("/classes", response_model=List[ClassResponse])
def get_all_classes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all classes for the current user's school. Only Admin can access.
    """
    # Only Admin can view classes
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can view classes"
        )
    
    classes = ClassService.get_all_classes_by_school(db, current_user["school_id"])
    return classes


@router.get("/classes/{class_id}", response_model=ClassResponse)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific class by ID. Only Admin can access.
    """
    # Only Admin can view classes
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can view classes"
        )
    
    class_obj = ClassService.get_class_by_id(db, class_id, current_user["school_id"])
    return class_obj


@router.put("/classes/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: int,
    request: ClassUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a class. Only Admin can update.
    """
    # Only Admin can update classes
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can update classes"
        )
    
    class_obj = ClassService.update_class(
        db=db,
        class_id=class_id,
        school_id=current_user["school_id"],
        class_name=request.class_name,
        is_active=request.is_active
    )
    
    return class_obj


@router.patch("/classes/{class_id}/status", response_model=ClassResponse)
def toggle_class_status(
    class_id: int,
    request: ClassStatusRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Toggle class active/inactive status. Only Admin can toggle.
    """
    # Only Admin can toggle class status
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can toggle class status"
        )
    
    class_obj = ClassService.toggle_class_status(
        db=db,
        class_id=class_id,
        school_id=current_user["school_id"],
        is_active=request.is_active
    )
    
    return class_obj


# ============= SECTION ENDPOINTS =============

@router.post("/sections", response_model=SectionResponse)
def create_section(
    request: SectionCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new section. Only Admin (RoleId=2) can create sections.
    """
    # Only Admin can create sections
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can create sections"
        )
    
    # Verify the class belongs to the admin's school
    class_obj = ClassService.get_class_by_id(db, request.class_id, current_user["school_id"])
    
    section = SectionService.create_section(
        db=db,
        class_id=request.class_id,
        section_name=request.section_name,
        class_teacher_id=request.class_teacher_id,
        school_id=current_user["school_id"]
    )
    
    return section


@router.get("/sections/class/{class_id}", response_model=List[SectionResponse])
def get_sections_by_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all sections for a specific class. Only Admin can access.
    """
    # Only Admin can view sections
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can view sections"
        )
    
    # Verify the class belongs to the admin's school
    class_obj = ClassService.get_class_by_id(db, class_id, current_user["school_id"])
    
    sections = SectionService.get_all_sections_by_class(db, class_id)
    return sections


@router.get("/sections/{section_id}", response_model=SectionResponse)
def get_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific section by ID. Only Admin can access.
    """
    # Only Admin can view sections
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can view sections"
        )
    
    section = SectionService.get_section_by_id(db, section_id)
    
    # Verify the section's class belongs to admin's school
    class_obj = ClassService.get_class_by_id(db, section.ClassId, current_user["school_id"])
    
    return section


@router.put("/sections/{section_id}", response_model=SectionResponse)
def update_section(
    section_id: int,
    request: SectionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a section. Only Admin can update.
    """
    # Only Admin can update sections
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can update sections"
        )
    
    section = SectionService.get_section_by_id(db, section_id)
    
    # Verify the section's class belongs to admin's school
    class_obj = ClassService.get_class_by_id(db, section.ClassId, current_user["school_id"])
    
    section = SectionService.update_section(
        db=db,
        section_id=section_id,
        section_name=request.section_name,
        class_teacher_id=request.class_teacher_id,
        is_active=request.is_active
    )
    
    return section


@router.patch("/sections/{section_id}/status", response_model=SectionResponse)
def toggle_section_status(
    section_id: int,
    request: SectionStatusRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Toggle section active/inactive status. Only Admin can toggle.
    """
    # Only Admin can toggle section status
    if current_user["role"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Only school administrators can toggle section status"
        )
    
    section = SectionService.get_section_by_id(db, section_id)
    
    # Verify the section's class belongs to admin's school
    class_obj = ClassService.get_class_by_id(db, section.ClassId, current_user["school_id"])
    
    section = SectionService.toggle_section_status(
        db=db,
        section_id=section_id,
        is_active=request.is_active
    )
    
    return section
