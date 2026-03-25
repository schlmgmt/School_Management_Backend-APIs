from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_schools: int
    active_schools: int
    total_admins: int
    total_students: int
    total_teachers: int

    class Config:
        json_schema_extra = {
            "example": {
                "total_schools": 10,
                "active_schools": 8,
                "total_admins": 10,
                "total_students": 500,
                "total_teachers": 50
            }
        }
