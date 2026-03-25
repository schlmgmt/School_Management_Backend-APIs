from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models.user import User
from ..db.models.school import School
from ..core.security import verify_password, create_access_token, create_refresh_token, decode_token, verify_password_reset_token, hash_password, generate_password_reset_token
from ..utils.email_service import send_forgot_password_email

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.Email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.Password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if school is active for non-super admin users (RoleId != 1)
    if user.RoleId != 1:  # 1 = Super Admin
        school = db.query(School).filter(School.SchoolId == user.SchoolId).first()
        
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        if not school.IsActive:
            raise HTTPException(
                status_code=403,
                detail="Your school is currently inactive. Please contact the administrator."
            )

    payload = {
        "user_id": user.UserId,
        "school_id": user.SchoolId,
        "role": user.RoleId
    }

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload)
    }

def refresh_access_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)

        return create_access_token({
            "user_id": payload["user_id"],
            "school_id": payload["school_id"],
            "role": payload["role"]
        })

    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def reset_password(db: Session, token: str, new_password: str, confirm_password: str):
    """
    Reset password using password reset token.
    Sets IsPasswordUpdated to True after successful password reset.
    """
    
    # Validate passwords match
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Validate password length
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    # Verify and decode the reset token
    payload = verify_password_reset_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired password reset link")
    
    user_id = payload.get("user_id")
    email = payload.get("email")
    
    # Find the user
    user = db.query(User).filter(User.UserId == user_id, User.Email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update password and set IsPasswordUpdated to True
    user.Password = hash_password(new_password)
    user.IsPasswordUpdated = True
    user.UpdatedAt = __import__('datetime').datetime.utcnow()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Password reset successfully. You can now login with your new password.",
        "user_id": user.UserId,
        "email": user.Email
    }


def forgot_password(db: Session, email: str, reset_password_base_url: str):
    """
    Handle forgot password request.
    Finds user by email, generates password reset token, and sends email.
    """
    
    # Find user by email
    user = db.query(User).filter(User.Email == email).first()
    if not user:
        # Return generic message for security (don't reveal if email exists)
        return {
            "message": "User With this email does not exists"
        }
    
    # Generate password reset token
    reset_token = generate_password_reset_token(user.UserId, user.Email)
    
    # Create reset password link
    reset_password_link = f"{reset_password_base_url}?token={reset_token}"
    
    # Send password reset email
    email_sent = send_forgot_password_email(
        user_email=user.Email,
        user_name=user.UserName,
        reset_password_link=reset_password_link
    )
    
    if not email_sent:
        print(f"Warning: Password reset email not sent to {user.Email}")
    
    return {
        "message": "A password reset link has been sent to your registered email address."
    }


def change_password(db: Session, user_id: int, current_password: str, new_password: str, confirm_new_password: str):
    """
    Change password for logged-in user.
    Requires verification of current password.
    """
    
    # Validate new passwords match
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    # Validate password length
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    # Validate new password is different from current password
    if current_password == new_password:
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    
    # Find the user
    user = db.query(User).filter(User.UserId == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(current_password, user.Password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    # Update password
    user.Password = hash_password(new_password)
    user.UpdatedAt = __import__('datetime').datetime.utcnow()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Password changed successfully.",
        "user_id": user.UserId,
        "email": user.Email
    }