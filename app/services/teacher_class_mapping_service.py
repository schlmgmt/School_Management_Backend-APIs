from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models.teacher_class_mapping import TeacherClassMapping
from ..db.models.teacher import Teacher
from ..db.models.class_model import Class
from ..db.models.section import Section
from datetime import datetime


class TeacherClassMappingService:
    """Service for Teacher-Class-Section mapping"""
    
    @staticmethod
    def create_mapping(db: Session, teacher_id: int, class_id: int, section_id: int, subject: str, school_id: int):
        """
        Create a new teacher-class-section mapping with subject.
        Validates that teacher, class, and section exist and belong to same school.
        Ensures the combination is unique.
        """
        # Verify teacher exists and belongs to the school
        teacher = db.query(Teacher).filter(Teacher.TeacherId == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        # Verify teacher's user belongs to the school
        from ..db.models.user import User
        teacher_user = db.query(User).filter(User.UserId == teacher.UserId).first()
        if not teacher_user or teacher_user.SchoolId != school_id:
            raise HTTPException(status_code=400, detail="Teacher does not belong to your school")
        
        # Verify class exists and belongs to the school
        class_obj = db.query(Class).filter(Class.ClassId == class_id, Class.SchoolId == school_id).first()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found in your school")
        
        # Verify section exists and belongs to the class
        section = db.query(Section).filter(Section.SectionId == section_id, Section.ClassId == class_id).first()
        if not section:
            raise HTTPException(status_code=404, detail="Section not found in this class")
        
        # Check if mapping already exists (unique composite key)
        existing_mapping = db.query(TeacherClassMapping).filter(
            TeacherClassMapping.TeacherId == teacher_id,
            TeacherClassMapping.ClassId == class_id,
            TeacherClassMapping.SectionId == section_id
        ).first()
        
        if existing_mapping:
            raise HTTPException(
                status_code=400,
                detail="This teacher is already assigned to this class and section"
            )
        
        # Create the mapping
        mapping = TeacherClassMapping(
            TeacherId=teacher_id,
            ClassId=class_id,
            SectionId=section_id,
            Subject=subject.strip()
        )
        
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        
        return mapping
    
    @staticmethod
    def get_mapping_by_id(db: Session, mapping_id: int):
        """Get a specific mapping by ID"""
        mapping = db.query(TeacherClassMapping).filter(
            TeacherClassMapping.TeacherClassMappingId == mapping_id
        ).first()
        
        if not mapping:
            raise HTTPException(status_code=404, detail="Mapping not found")
        
        return mapping
    
    @staticmethod
    def get_mappings_by_teacher(db: Session, teacher_id: int):
        """
        Get all class-section assignments for a specific teacher.
        """
        mappings = db.query(TeacherClassMapping).filter(
            TeacherClassMapping.TeacherId == teacher_id
        ).all()
        
        return mappings
    
    @staticmethod
    def get_all_mappings_by_school(db: Session, school_id: int):
        """
        Get all mappings for a school (all teachers' assignments).
        """
        from ..db.models.user import User
        
        # Get all teachers in the school
        teachers_in_school = db.query(Teacher).join(
            User, Teacher.UserId == User.UserId
        ).filter(User.SchoolId == school_id).all()
        
        teacher_ids = [t.TeacherId for t in teachers_in_school]
        
        if not teacher_ids:
            return []
        
        # Get all mappings for these teachers
        mappings = db.query(TeacherClassMapping).filter(
            TeacherClassMapping.TeacherId.in_(teacher_ids)
        ).all()
        
        return mappings
    
    @staticmethod
    def delete_mapping(db: Session, mapping_id: int):
        """
        Delete a teacher-class-section mapping.
        """
        mapping = TeacherClassMappingService.get_mapping_by_id(db, mapping_id)
        
        db.delete(mapping)
        db.commit()
        
        return {"message": "Mapping deleted successfully", "mapping_id": mapping_id}
