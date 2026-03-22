from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, user_routes, school_routes
from app.db.database import engine
from app.db.base import Base
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.school import School

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management Multi-Tenant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1")
app.include_router(school_routes.router, prefix="/api/v1")