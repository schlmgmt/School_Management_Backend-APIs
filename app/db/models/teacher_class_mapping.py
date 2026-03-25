from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from ..base import Base


class TeacherClassMapping(Base):
    __tablename__ = "teacher_class_mappings"

    TeacherClassMappingId = Column(Integer, primary_key=True, index=True)
    TeacherId = Column(Integer, ForeignKey("teachers.TeacherId"), nullable=False, index=True)
    ClassId = Column(Integer, ForeignKey("classes.ClassId"), nullable=False, index=True)
    SectionId = Column(Integer, ForeignKey("sections.SectionId"), nullable=False, index=True)
    Subject = Column(String(200), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Composite unique constraint: Teacher, Class, Section combination must be unique
    __table_args__ = (
        UniqueConstraint('TeacherId', 'ClassId', 'SectionId', name='unique_teacher_class_section'),
    )
