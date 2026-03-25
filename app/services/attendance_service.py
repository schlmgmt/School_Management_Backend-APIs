from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date, datetime
from typing import List
from ..db.models.attendance import Attendance, AttendanceStatus
from ..db.models.student import Student
from ..db.models.class_model import Class
from ..db.models.section import Section
from ..db.models.teacher import Teacher
from ..db.models.user import User
from ..db.models.teacher_class_mapping import TeacherClassMapping


class AttendanceService:
    """Service for Attendance management"""
    
    @staticmethod
    def mark_attendance(
        db: Session,
        class_id: int,
        section_id: int,
        date_obj: date,
        students: List[dict],
        teacher_id: int,
        school_id: int
    ):
        """
        Mark attendance for multiple students in a class/section.
        Only class teacher of the section can mark attendance.
        
        Validates:
        - Class exists and belongs to school
        - Section exists and belongs to class
        - Teacher is the class teacher of the section
        - Each student exists and belongs to school
        - No duplicate attendance for each student on same day
        
        Returns list of created attendance records
        """
        # Verify class exists and belongs to school
        class_obj = db.query(Class).filter(Class.ClassId == class_id, Class.SchoolId == school_id).first()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found in your school")
        
        # Verify section exists and belongs to class
        section = db.query(Section).filter(
            Section.SectionId == section_id,
            Section.ClassId == class_id
        ).first()
        
        if not section:
            raise HTTPException(status_code=404, detail="Section not found in this class")
        
        # Verify teacher is the class teacher of this section
        if section.ClassTeacherId != teacher_id:
            raise HTTPException(
                status_code=403,
                detail="You are not the class teacher for this section. Only class teacher can mark attendance."
            )
        
        attendance_records = []
        errors = []
        
        # Process each student
        for student_entry in students:
            student_id = student_entry["student_id"]
            status = student_entry["status"]
            
            try:
                # Verify student exists
                student = db.query(Student).filter(Student.StudentId == student_id).first()
                if not student:
                    errors.append({"student_id": student_id, "error": "Student not found"})
                    continue
                
                # Verify student belongs to school
                student_user = db.query(User).filter(
                    User.UserId == student.UserId,
                    User.SchoolId == school_id
                ).first()
                if not student_user:
                    errors.append({"student_id": student_id, "error": "Student does not belong to your school"})
                    continue
                
                # Check if attendance already exists for this student on this day
                existing_attendance = db.query(Attendance).filter(
                    Attendance.StudentId == student_id,
                    Attendance.Date == date_obj
                ).first()
                
                if existing_attendance:
                    errors.append({"student_id": student_id, "error": "Attendance already marked for this date"})
                    continue
                
                # Create attendance record
                attendance = Attendance(
                    StudentId=student_id,
                    ClassId=class_id,
                    SectionId=section_id,
                    Date=date_obj,
                    Status=status,
                    MarkedBy=teacher_id
                )
                
                db.add(attendance)
                attendance_records.append(attendance)
                
            except Exception as e:
                errors.append({"student_id": student_id, "error": str(e)})
        
        # Commit all records
        if attendance_records:
            db.commit()
            for record in attendance_records:
                db.refresh(record)
        
        # Return results with any errors
        return {
            "success_count": len(attendance_records),
            "error_count": len(errors),
            "attendance_records": attendance_records,
            "errors": errors if errors else None
        }
    
    @staticmethod
    def get_attendance_by_class_date(
        db: Session,
        class_id: int,
        section_id: int,
        date_obj: date,
        teacher_id: int,
        school_id: int
    ):
        """
        Get attendance for a class section on a specific date.
        Teacher must be assigned to teach this class-section.
        """
        # Verify teacher is assigned to this class-section
        mapping = db.query(TeacherClassMapping).filter(
            TeacherClassMapping.TeacherId == db.query(Teacher).filter(Teacher.TeacherId == teacher_id).first().TeacherId,
            TeacherClassMapping.ClassId == class_id,
            TeacherClassMapping.SectionId == section_id
        ).first()
        
        if not mapping:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to teach this class and section"
            )
        
        # Get attendance records
        attendance_records = db.query(Attendance).filter(
            Attendance.ClassId == class_id,
            Attendance.SectionId == section_id,
            Attendance.Date == date_obj
        ).all()
        
        return attendance_records
    
    @staticmethod
    def get_student_attendance_history(
        db: Session,
        student_id: int,
        school_id: int
    ):
        """
        Get attendance history for a student.
        """
        # Verify student exists and belongs to school
        student = db.query(Student).filter(Student.StudentId == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        student_user = db.query(User).filter(User.UserId == student.UserId, User.SchoolId == school_id).first()
        if not student_user:
            raise HTTPException(status_code=403, detail="Student does not belong to your school")
        
        # Get all attendance records for student
        attendance_records = db.query(Attendance).filter(
            Attendance.StudentId == student_id
        ).order_by(Attendance.Date.desc()).all()
        
        return attendance_records
    
    @staticmethod
    def update_attendance(
        db: Session,
        attendance_id: int,
        status: str,
        teacher_id: int,
        school_id: int
    ):
        """
        Update attendance status.
        Only the class teacher who marked it can update.
        """
        # Get attendance record
        attendance = db.query(Attendance).filter(Attendance.AttendanceId == attendance_id).first()
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        # Get the section to check class teacher
        section = db.query(Section).filter(Section.SectionId == attendance.SectionId).first()
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        
        # Verify teacher is the class teacher of this section
        if section.ClassTeacherId != teacher_id:
            raise HTTPException(
                status_code=403,
                detail="Only the class teacher can update attendance"
            )
        
        # Update status
        attendance.Status = status  # Status is already an enum value from the request
        attendance.UpdatedAt = datetime.utcnow()
        
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        
        return attendance
    
    @staticmethod
    def get_attendance_by_id(db: Session, attendance_id: int):
        """Get a specific attendance record by ID"""
        attendance = db.query(Attendance).filter(Attendance.AttendanceId == attendance_id).first()
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return attendance
