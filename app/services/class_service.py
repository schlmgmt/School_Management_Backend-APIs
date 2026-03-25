from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models.class_model import Class
from ..db.models.section import Section
from datetime import datetime


class ClassService:
    """Service for Class management"""
    
    @staticmethod
    def create_class(db: Session, school_id: int, class_name: str):
        """
        Create a new class for a school.
        """
        # Check if class with same name already exists in this school
        existing_class = db.query(Class).filter(
            Class.SchoolId == school_id,
            Class.ClassName == class_name
        ).first()
        
        if existing_class:
            raise HTTPException(
                status_code=400,
                detail=f"Class '{class_name}' already exists in this school"
            )
        
        class_obj = Class(
            SchoolId=school_id,
            ClassName=class_name.strip(),
            IsActive=True
        )
        
        db.add(class_obj)
        db.commit()
        db.refresh(class_obj)
        
        return class_obj
    
    @staticmethod
    def get_class_by_id(db: Session, class_id: int, school_id: int = None):
        """
        Get a class by ID. Optionally verify it belongs to a school.
        """
        query = db.query(Class).filter(Class.ClassId == class_id)
        
        if school_id:
            query = query.filter(Class.SchoolId == school_id)
        
        class_obj = query.first()
        
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")
        
        return class_obj
    
    @staticmethod
    def get_all_classes_by_school(db: Session, school_id: int):
        """
        Get all classes for a school.
        """
        classes = db.query(Class).filter(Class.SchoolId == school_id).all()
        return classes
    
    @staticmethod
    def update_class(db: Session, class_id: int, school_id: int, class_name: str = None, is_active: bool = None):
        """
        Update a class.
        """
        class_obj = ClassService.get_class_by_id(db, class_id, school_id)
        
        # If updating class name, check for duplicates
        if class_name and class_name != class_obj.ClassName:
            existing_class = db.query(Class).filter(
                Class.SchoolId == school_id,
                Class.ClassName == class_name,
                Class.ClassId != class_id
            ).first()
            
            if existing_class:
                raise HTTPException(
                    status_code=400,
                    detail=f"Class '{class_name}' already exists in this school"
                )
            
            class_obj.ClassName = class_name.strip()
        
        if is_active is not None:
            class_obj.IsActive = is_active
        
        class_obj.UpdatedAt = datetime.utcnow()
        
        db.add(class_obj)
        db.commit()
        db.refresh(class_obj)
        
        return class_obj
    
    @staticmethod
    def toggle_class_status(db: Session, class_id: int, school_id: int, is_active: bool):
        """
        Toggle class active/inactive status.
        """
        class_obj = ClassService.get_class_by_id(db, class_id, school_id)
        
        class_obj.IsActive = is_active
        class_obj.UpdatedAt = datetime.utcnow()
        
        db.add(class_obj)
        db.commit()
        db.refresh(class_obj)
        
        return class_obj


class SectionService:
    """Service for Section management"""
    
    @staticmethod
    def create_section(db: Session, class_id: int, section_name: str, class_teacher_id: int, school_id: int = None):
        """
        Create a new section for a class with a class teacher.
        """
        # Verify class exists
        class_obj = db.query(Class).filter(Class.ClassId == class_id).first()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")
        
        # Verify class teacher exists
        teacher = db.query(Teacher).filter(Teacher.TeacherId == class_teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        # If school_id provided, verify teacher belongs to that school
        if school_id:
            from ..db.models.user import User
            teacher_user = db.query(User).filter(User.UserId == teacher.UserId, User.SchoolId == school_id).first()
            if not teacher_user:
                raise HTTPException(status_code=400, detail="Class teacher does not belong to your school")
        
        # Check if section with same name already exists in this class
        existing_section = db.query(Section).filter(
            Section.ClassId == class_id,
            Section.SectionName == section_name
        ).first()
        
        if existing_section:
            raise HTTPException(
                status_code=400,
                detail=f"Section '{section_name}' already exists in this class"
            )
        
        section = Section(
            ClassId=class_id,
            ClassTeacherId=class_teacher_id,
            SectionName=section_name.strip(),
            IsActive=True
        )
        
        db.add(section)
        db.commit()
        db.refresh(section)
        
        return section
    
    @staticmethod
    def get_section_by_id(db: Session, section_id: int):
        """
        Get a section by ID.
        """
        section = db.query(Section).filter(Section.SectionId == section_id).first()
        
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        
        return section
    
    @staticmethod
    def get_all_sections_by_class(db: Session, class_id: int):
        """
        Get all sections for a class.
        """
        sections = db.query(Section).filter(Section.ClassId == class_id).all()
        return sections
    
    @staticmethod
    def update_section(db: Session, section_id: int, section_name: str = None, class_teacher_id: int = None, is_active: bool = None):
        """
        Update a section.
        """
        section = SectionService.get_section_by_id(db, section_id)
        
        # If updating section name, check for duplicates in same class
        if section_name and section_name != section.SectionName:
            existing_section = db.query(Section).filter(
                Section.ClassId == section.ClassId,
                Section.SectionName == section_name,
                Section.SectionId != section_id
            ).first()
            
            if existing_section:
                raise HTTPException(
                    status_code=400,
                    detail=f"Section '{section_name}' already exists in this class"
                )
            
            section.SectionName = section_name.strip()
        
        # If updating class teacher, verify teacher exists
        if class_teacher_id is not None:
            teacher = db.query(Teacher).filter(Teacher.TeacherId == class_teacher_id).first()
            if not teacher:
                raise HTTPException(status_code=404, detail="Teacher not found")
            
            section.ClassTeacherId = class_teacher_id
        
        if is_active is not None:
            section.IsActive = is_active
        
        section.UpdatedAt = datetime.utcnow()
        
        db.add(section)
        db.commit()
        db.refresh(section)
        
        return section
    
    @staticmethod
    def toggle_section_status(db: Session, section_id: int, is_active: bool):
        """
        Toggle section active/inactive status.
        """
        section = SectionService.get_section_by_id(db, section_id)
        
        section.IsActive = is_active
        section.UpdatedAt = datetime.utcnow()
        
        db.add(section)
        db.commit()
        db.refresh(section)
        
        return section
