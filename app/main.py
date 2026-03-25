from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, user_routes, school_routes, dashboard_routes, student_routes, teacher_routes, class_routes, teacher_class_mapping_routes, attendance_routes
from app.db.database import engine
from app.db.base import Base
# Import models to register them with SQLAlchemy
from app.db.models.user import User
from app.db.models.school import School
from app.db.models.role import Role
from app.db.models.student import Student
from app.db.models.teacher import Teacher
from app.db.models.class_model import Class
from app.db.models.section import Section
from app.db.models.teacher_class_mapping import TeacherClassMapping
from app.db.models.attendance import Attendance

app = FastAPI(title="School Management Multi-Tenant API")

# ✅ Move DB init here (safe)
@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ DB connected")
    except Exception as e:
        print("❌ DB connection failed:", e)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1")
app.include_router(school_routes.router, prefix="/api/v1")
app.include_router(dashboard_routes.router, prefix="/api/v1")
app.include_router(student_routes.router, prefix="/api/v1")
app.include_router(teacher_routes.router, prefix="/api/v1")
app.include_router(class_routes.router)
app.include_router(teacher_class_mapping_routes.router)
app.include_router(attendance_routes.router)