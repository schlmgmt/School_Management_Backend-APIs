"""
Script to seed the roles table with initial data
Run this after the database tables are created
"""
from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.db.models.role import Role


def seed_roles():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Define the roles
        roles_data = [
            {"RoleId": 1, "RoleName": "Super Admin", "Description": "Super Administrator with full access"},
            {"RoleId": 2, "RoleName": "Admin", "Description": "Administrator"},
            {"RoleId": 3, "RoleName": "Teacher", "Description": "Teacher"},
            {"RoleId": 4, "RoleName": "Student", "Description": "Student"},
        ]
        
        # Check if roles already exist
        existing_roles = db.query(Role).count()
        
        if existing_roles == 0:
            print("Adding roles...")
            for role_data in roles_data:
                role = Role(**role_data)
                db.add(role)
            
            db.commit()
            print("✓ Roles added successfully!")
            for role_data in roles_data:
                print(f"  - {role_data['RoleName']} (ID: {role_data['RoleId']})")
        else:
            print(f"Roles already exist in database ({existing_roles} roles found)")
            
    except Exception as e:
        db.rollback()
        print(f"✗ Error adding roles: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()
