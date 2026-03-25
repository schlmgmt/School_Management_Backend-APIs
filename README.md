# School Management System - Backend

A comprehensive backend API for managing schools, admins, users, and authentication. Built with FastAPI, SQLAlchemy, and PostgreSQL.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Database](#database)
- [Running the Application](#running-the-application)

---

## ✨ Features

### School Management
- Create new schools
- List all schools
- Only Super Admin can manage schools

### Admin Management
- Super Admin creates school admins
- Automatic email notification with password reset link
- Token-based secure onboarding

### Authentication & Authorization
- JWT-based token authentication
- Role-based access control (RBAC)
- Refresh token support
- Secure password hashing with bcrypt

### Password Management
- **Forgot Password**: Users can request password reset
- **Reset Password**: Token-based password reset from email
- **Change Password**: Logged-in users can change their password
- All passwords are bcrypt hashed

### Email Notifications
- Admin onboarding emails
- Forgot password emails
- Password reset links with 24-hour expiration
- HTML formatted professional emails

### Student & Teacher Management
- Create and manage students with email onboarding
- Create and manage teachers with public profiles
- Track student enrollment, roll numbers, and dates of birth
- Student and teacher status management

### Class & Section Management
- Organize students into classes and sections
- Assign class teachers to sections
- Track class and section activity status
- Hierarchical class structure

### Teacher-Class Assignments
- Assign teachers to specific classes and sections
- Track subject assignments
- Maintain unique mapping constraints
- Support multi-section teaching

### Attendance System
- Bulk attendance marking for multiple students
- Class-date-based attendance tracking
- Duplicate attendance prevention (one per student per day)
- Role-based access (class teachers only)
- Attendance history tracking and retrieval
- Status tracking (present/absent)

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: Bcrypt
- **Email**: SMTP (Gmail)
- **Python**: 3.8+

---

## 📁 Project Structure

```
schl_mgmt_bknd/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   │
│   ├── core/
│   │   ├── config.py           # Configuration & environment settings
│   │   ├── dependencies.py     # Dependency injection
│   │   └── security.py         # JWT & password utilities
│   │
│   ├── db/
│   │   ├── base.py             # Base model
│   │   ├── database.py         # Database session
│   │   └── models/
│   │       ├── user.py         # User model
│   │       ├── school.py       # School model
│   │       ├── role.py         # Role model
│   │       ├── student.py      # Student model
│   │       ├── teacher.py      # Teacher model
│   │       ├── class_model.py  # Class model
│   │       ├── section.py      # Section model
│   │       ├── teacher_class_mapping.py  # Teacher-Class assignment
│   │       └── attendance.py   # Attendance model
│   │
│   ├── schemas/
│   │   ├── input/              # Request schemas
│   │   │   ├── auth_input.py
│   │   │   ├── school_input.py
│   │   │   ├── admin_input.py
│   │   │   ├── student_input.py
│   │   │   ├── teacher_input.py
│   │   │   ├── class_input.py
│   │   │   ├── teacher_class_mapping_input.py
│   │   │   └── attendance_input.py
│   │   └── output/             # Response schemas
│   │       ├── auth_output.py
│   │       ├── school_output.py
│   │       ├── admin_output.py
│   │       ├── student_output.py
│   │       ├── teacher_output.py
│   │       ├── class_output.py
│   │       └── attendance_output.py
│   │
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── school_service.py
│   │   ├── user_service.py
│   │   ├── student_service.py
│   │   ├── teacher_service.py
│   │   ├── class_service.py
│   │   ├── teacher_class_mapping_service.py
│   │   └── attendance_service.py
│   │
│   ├── routes/                 # API endpoints
│   │   ├── auth_routes.py
│   │   ├── school_routes.py
│   │   ├── user_routes.py
│   │   ├── student_routes.py
│   │   ├── teacher_routes.py
│   │   ├── class_routes.py
│   │   ├── teacher_class_mapping_routes.py
│   │   └── attendance_routes.py
│   │
│   └── utils/
│       ├── common.py           # Common utilities
│       └── email_service.py    # Email sending
│
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── seed_roles.py              # Initial role seeding script
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
cd c:\Users\Dev\Desktop\coding\School_Management\schl_mgmt_bknd
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy and update the `.env` file with your settings:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-secret-key-here

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Algorithm
ALGORITHM=HS256

# Email SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

### 5. Database Setup

Ensure your PostgreSQL database is running and tables are created. The models are defined in `app/db/models/`.

### 6. Initialize Roles (Optional)

```bash
python seed_roles.py
```

---

## 🔐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT secret key for token signing | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token validity in minutes | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token validity in days | `7` |
| `SMTP_SERVER` | Email server address | `smtp.gmail.com` |
| `SMTP_PORT` | Email server port | `587` |
| `SENDER_EMAIL` | Email account to send from | `your-email@gmail.com` |
| `SENDER_PASSWORD` | Email account password/app-password | `xxxx xxxx xxxx xxxx` |

**Note**: For Gmail, use [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

---

## 📡 API Endpoints

### Authentication Routes (`/auth`)

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Refresh Token
```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}

Response:
{
  "access_token": "eyJ..."
}
```

#### Forgot Password
```
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}

Response:
{
  "message": "If an account with this email exists, a password reset link has been sent."
}
```

#### Reset Password
```
POST /auth/reset-password
Content-Type: application/json

{
  "token": "eyJ...",
  "new_password": "NewPassword@123",
  "confirm_password": "NewPassword@123"
}

Response:
{
  "message": "Password reset successfully. You can now login with your new password.",
  "user_id": 5,
  "email": "user@example.com"
}
```

#### Change Password
```
POST /auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "OldPassword@123",
  "new_password": "NewPassword@456",
  "confirm_new_password": "NewPassword@456"
}

Response:
{
  "message": "Password changed successfully.",
  "user_id": 5,
  "email": "user@example.com"
}
```

### School Routes (`/schools`)

#### Create School (Super Admin only)
```
POST /schools
Authorization: Bearer <super_admin_token>
Content-Type: application/json

{
  "school_name": "St. Mary's School",
  "address": "123 Main Street",
  "phone_number": "555-1234",
  "email": "contact@stmarys.com"
}

Response:
{
  "school_id": 1,
  "school_name": "St. Mary's School",
  "address": "123 Main Street",
  "phone_number": "555-1234",
  "email": "contact@stmarys.com",
  "is_active": true,
  "created_at": "2024-03-22T10:30:00"
}
```

#### List All Schools (Super Admin only)
```
GET /schools
Authorization: Bearer <super_admin_token>

Response:
[
  {
    "school_id": 1,
    "school_name": "St. Mary's School",
    "address": "123 Main Street",
    "phone_number": "555-1234",
    "email": "contact@stmarys.com",
    "is_active": true,
    "created_at": "2024-03-22T10:30:00"
  }
]
```

#### Create School Admin (Super Admin only)
```
POST /schools/{school_id}/admin
Authorization: Bearer <super_admin_token>
Content-Type: application/json

{
  "admin_name": "John Doe",
  "admin_email": "admin@school.com",
  "phone_number": "555-5678",
  "school_id": 1
}

Response:
{
  "user_id": 5,
  "user_name": "John Doe",
  "school_id": 1,
  "email": "admin@school.com",
  "phone_number": "555-5678",
  "role_id": 2,
  "is_password_updated": false,
  "created_at": "2024-03-22T10:35:00",
  "message": "Admin created successfully. Onboarding email has been sent."
}
```

### Student Routes (`/students`)

#### Create Student (Admin only)
```
POST /students
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "user_name": "John Smith",
  "email": "john@example.com",
  "class_id": 1,
  "section_id": 1,
  "roll_number": "10001",
  "date_of_birth": "2010-05-15",
  "admission_date": "2023-06-01"
}

Response:
{
  "student_id": 1,
  "user_id": 10,
  "user_name": "John Smith",
  "email": "john@example.com",
  "class_id": 1,
  "section_id": 1,
  "roll_number": "10001",
  "date_of_birth": "2010-05-15",
  "admission_date": "2023-06-01",
  "is_active": true,
  "created_at": "2024-03-22T10:35:00",
  "message": "Student created successfully. Onboarding email has been sent."
}
```

#### List Students (Admin gets all, Student gets own)
```
GET /students
Authorization: Bearer <token>

Response:
[
  {
    "student_id": 1,
    "user_name": "John Smith",
    "email": "john@example.com",
    "class_id": 1,
    "section_id": 1,
    "roll_number": "10001"
  }
]
```

### Teacher Routes (`/teachers`)

#### Create Teacher (Admin only)
```
POST /teachers
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "user_name": "Jane Doe",
  "email": "jane@example.com",
  "specialization": "Mathematics",
  "date_of_joining": "2023-06-01"
}

Response:
{
  "teacher_id": 1,
  "user_id": 11,
  "user_name": "Jane Doe",
  "email": "jane@example.com",
  "specialization": "Mathematics",
  "date_of_joining": "2023-06-01",
  "is_active": true,
  "created_at": "2024-03-22T10:35:00",
  "message": "Teacher created successfully. Onboarding email has been sent."
}
```

#### List Teachers (Public - Everyone can view)
```
GET /teachers

Response:
[
  {
    "teacher_id": 1,
    "user_name": "Jane Doe",
    "email": "jane@example.com",
    "specialization": "Mathematics"
  }
]
```

### Class Routes (`/classes`)

#### Create Class (Admin only)
```
POST /classes
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "class_name": "10th Grade",
  "is_active": true
}

Response:
{
  "class_id": 1,
  "school_id": 1,
  "class_name": "10th Grade",
  "is_active": true,
  "created_at": "2024-03-22T10:35:00"
}
```

### Section Routes (`/sections`)

#### Create Section (Admin only)
```
POST /sections
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "class_id": 1,
  "section_name": "A",
  "class_teacher_id": 1
}

Response:
{
  "section_id": 1,
  "class_id": 1,
  "class_teacher_id": 1,
  "section_name": "A",
  "is_active": true,
  "created_at": "2024-03-22T10:35:00"
}
```

### Attendance Routes (`/api/v1/attendance`)

#### Mark Attendance (Class Teacher only)
```
POST /api/v1/attendance
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "class_id": 1,
  "section_id": 1,
  "date": "2026-03-25",
  "students": [
    { "student_id": 1, "status": "present" },
    { "student_id": 2, "status": "absent" },
    { "student_id": 3, "status": "present" }
  ]
}

Response:
{
  "class_id": 1,
  "section_id": 1,
  "date": "2026-03-25",
  "total_marked": 3,
  "attendance_records": [
    {
      "attendance_id": 1,
      "student_id": 1,
      "class_id": 1,
      "section_id": 1,
      "date": "2026-03-25",
      "status": "present",
      "marked_by": 5,
      "created_at": "2024-03-22T10:35:00",
      "updated_at": "2024-03-22T10:35:00"
    },
    ...
  ]
}
```

#### Get Attendance (Class Teacher only)
```
GET /api/v1/attendance?class_id=1&section_id=1&date=2026-03-25
Authorization: Bearer <teacher_token>

Response:
[
  {
    "attendance_id": 1,
    "student_id": 1,
    "class_id": 1,
    "section_id": 1,
    "date": "2026-03-25",
    "status": "present",
    "marked_by": 5,
    "created_at": "2024-03-22T10:35:00"
  }
]
```

#### Get Student Attendance History (Teacher/Admin)
```
GET /api/v1/attendance/student/{student_id}
Authorization: Bearer <token>

Response:
[
  {
    "attendance_id": 1,
    "student_id": 1,
    "class_id": 1,
    "section_id": 1,
    "date": "2026-03-25",
    "status": "present",
    "marked_by": 5,
    "created_at": "2024-03-22T10:35:00"
  },
  {
    "attendance_id": 2,
    "student_id": 1,
    "class_id": 1,
    "section_id": 1,
    "date": "2026-03-24",
    "status": "absent",
    "marked_by": 5,
    "created_at": "2024-03-22T10:30:00"
  }
]
```

#### Update Attendance Status (Class Teacher only)
```
PUT /api/v1/attendance
Authorization: Bearer <teacher_token>
Content-Type: application/json

{
  "attendance_id": 1,
  "status": "absent"
}

Response:
{
  "attendance_id": 1,
  "student_id": 1,
  "class_id": 1,
  "section_id": 1,
  "date": "2026-03-25",
  "status": "absent",
  "marked_by": 5,
  "created_at": "2024-03-22T10:35:00",
  "updated_at": "2024-03-22T10:40:00"
}
```

---

## 🔐 Authentication

### Token Structure

Tokens are JWT-based containing:
- `user_id`: Unique user identifier
- `school_id`: Associated school ID
- `role`: User role ID
- `exp`: Token expiration time
- `force_exp`: Force expiration timestamp

### Role-Based Access Control

| Role ID | Role Name | Permissions |
|---------|-----------|-------------|
| 1 | Super Admin | All permissions |
| 2 | School Admin | School-specific operations |
| 3 | Teacher | Teaching-related operations |
| 4 | Student | Student-specific operations |

### How to Use Bearer Token

Include the access token in the `Authorization` header:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 💾 Database

### Models

#### User Model
```python
UserId             # Primary key
UserName           # User's name
SchoolId           # Foreign key to school
ClassId            # Class assignment
SectionId          # Section assignment
RoleId             # User role (1-4)
Email              # Unique email
Password           # Hashed password
PhoneNumber        # Contact number
IsPasswordUpdated  # Onboarding status
CreatedAt          # Creation timestamp
UpdatedAt          # Last update timestamp
CreatedBy          # Created by user ID
UpdatedBy          # Updated by user ID
```

#### School Model
```python
SchoolId      # Primary key
SchoolName    # School name (unique)
Address       # School address
PhoneNumber   # Contact number
Email         # Contact email (unique)
IsActive      # Active status
CreatedAt     # Creation timestamp
UpdatedAt     # Last update timestamp
```

#### Role Model
```python
RoleId      # Primary key
RoleName    # Role name (unique)
Description # Role description
CreatedAt   # Creation timestamp
UpdatedAt   # Last update timestamp
```

#### Student Model
```python
StudentId         # Primary key
UserId            # Foreign key to User
Email             # Email address (unique)
ClassId           # Foreign key to Class
SectionId         # Foreign key to Section
RollNumber        # Student roll number
DateOfBirth       # Date of birth
AdmissionDate     # Admission date
IsActive          # Active status
CreatedAt         # Creation timestamp
UpdatedAt         # Last update timestamp
```

#### Teacher Model
```python
TeacherId         # Primary key
UserId            # Foreign key to User
Email             # Email address (unique)
Specialization    # Subject/specialization
DateOfJoining     # Joining date
IsActive          # Active status
CreatedAt         # Creation timestamp
UpdatedAt         # Last update timestamp
```

#### Class Model
```python
ClassId           # Primary key
SchoolId          # Foreign key to School
ClassName         # Class name (e.g., "10th", "12th")
IsActive          # Active status
CreatedAt         # Creation timestamp
UpdatedAt         # Last update timestamp
```

#### Section Model
```python
SectionId         # Primary key
ClassId           # Foreign key to Class
ClassTeacherId    # Foreign key to Teacher (class teacher)
SectionName       # Section name (e.g., "A", "B", "C")
IsActive          # Active status
CreatedAt         # Creation timestamp
UpdatedAt         # Last update timestamp
```

#### TeacherClassMapping Model
```python
TeacherClassMappingId  # Primary key
TeacherId              # Foreign key to Teacher
ClassId                # Foreign key to Class
SectionId              # Foreign key to Section
Subject                # Subject taught
CreatedAt              # Creation timestamp
UpdatedAt              # Last update timestamp
Unique Constraint: (TeacherId, ClassId, SectionId)
```

#### Attendance Model
```python
AttendanceId      # Primary key
StudentId         # Foreign key to Student
ClassId           # Foreign key to Class
SectionId         # Foreign key to Section
Date              # Attendance date
Status            # Attendance status (present/absent)
MarkedBy          # Foreign key to Teacher who marked
CreatedAt         # Creation timestamp
UpdatedAt         # Last update timestamp
Unique Constraint: (StudentId, Date)
```

---

## ▶️ Running the Application

### Start Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload

# Or using the terminal command
# Open terminal and run: uvicorn app.main:app --reload
```

The application will be available at: `http://localhost:8000`

### API Documentation

Once running, view interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing the API

Using cURL:

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Create School (requires super admin token)
curl -X POST http://localhost:8000/schools \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "school_name":"School Name",
    "address":"Address",
    "phone_number":"555-1234",
    "email":"school@example.com"
  }'
```

Using PowerShell:

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    email = "user@example.com"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
    -Method Post `
    -Headers $headers `
    -Body $body

$response | ConvertTo-Json
```

---

## 🔗 Important Endpoints Summary

### No Authentication Required
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token
- `GET /teachers` - List all teachers

### Authentication Required (Admin only)
- `POST /auth/change-password` - Change password (logged-in user)
- `POST /schools` - Create school (Super Admin only)
- `GET /schools` - List schools (Super Admin only)
- `POST /schools/{school_id}/admin` - Create admin (Super Admin only)
- `POST /students` - Create student
- `GET /students` - List students (admin: all, student: self)
- `POST /teachers` - Create teacher
- `POST /classes` - Create class
- `GET /classes` - List classes
- `POST /sections` - Create section
- `GET /sections` - List sections
- `POST /api/v1/teacher-class-mapping` - Assign teacher to class

### Authentication Required (Teacher only)
- `POST /api/v1/attendance` - Mark attendance (class teacher only)
- `GET /api/v1/attendance` - Get attendance by class/date (assigned teacher)
- `PUT /api/v1/attendance` - Update attendance (class teacher only)

### Authentication Required (Teacher/Admin)
- `GET /api/v1/attendance/student/{student_id}` - Get student attendance history

---

## 📝 Configuration Notes

1. **Reset Password URL**: Update `reset_password_base_url` in routes files to point to your frontend password reset form

2. **Email Configuration**: For Gmail:
   - Enable 2-factor authentication
   - Generate app-specific password
   - Use that password in `.env` file

3. **Database**: Ensure PostgreSQL is running and connection string is correct

4. **Secret Key**: Use a strong, random secret key in production

---

## 🤝 Features Overview

### Password Management Flow

1. **New Admin Creation** (`/schools/{id}/admin`)
   - Super Admin creates admin
   - Reset link sent via email
   - Admin sets password via `/auth/reset-password`

2. **Forgot Password** (`/auth/forgot-password`)
   - User requests password reset
   - Reset link sent via email
   - User sets new password via `/auth/reset-password`

3. **Change Password** (`/auth/change-password`)
   - Logged-in user changes own password
   - Requires current password verification

---

## 📦 Dependencies

See `requirements.txt` for complete list. Key packages:
- fastapi
- sqlalchemy
- psycopg2-binary (PostgreSQL)
- pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart

---

## ⚠️ Important Notes

1. All passwords are hashed using bcrypt
2. Tokens expire after specified time
3. Reset links valid for 24 hours
4. Email notifications require SMTP configuration
5. Database connection must be established before running
6. Super Admin account must exist for school/admin creation

---

## 🐛 Troubleshooting

### Email Not Sending
- Check SMTP credentials in `.env`
- Verify firewall allows SMTP port 587
- For Gmail, ensure app-specific password is used

### Database Connection Error
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Ensure database exists

### Token Invalid
- Check SECRET_KEY is set correctly
- Ensure token is not expired
- Verify Bearer token format in header

---

## 📄 License

This project is part of the School Management System.

---

## 👨‍💼 Support

For issues or questions, contact the development team.

---

**Last Updated**: March 22, 2026  
**Version**: 1.0.0
