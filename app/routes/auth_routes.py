from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.input.auth_input import LoginRequest, RefreshTokenRequest, ResetPasswordRequest, ForgotPasswordRequest, ChangePasswordRequest
from ..schemas.output.auth_output import TokenResponse
from ..services.auth_service import login_user, refresh_access_token, reset_password, forgot_password, change_password
from ..core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)

@router.post("/refresh")
def refresh(data: RefreshTokenRequest):
    return {"access_token": refresh_access_token(data.refresh_token)}

@router.post("/reset-password")
def reset_password_endpoint(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password using the password reset token sent via email.
    This endpoint sets IsPasswordUpdated to True.
    """
    return reset_password(db, data.token, data.new_password, data.confirm_password)

@router.post("/forgot-password")
def forgot_password_endpoint(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Initiate forgot password process.
    Sends password reset link to the email address.
    No authentication required.
    """
    reset_password_base_url = "exp://localhost/reset-password"  # Update with your actual frontend URL
    
    return forgot_password(db, data.email, reset_password_base_url)

@router.post("/change-password")
def change_password_endpoint(data: ChangePasswordRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Change password for logged-in user.
    Requires current password verification.
    Authentication required.
    """
    return change_password(
        db=db,
        user_id=user.get("user_id"),
        current_password=data.current_password,
        new_password=data.new_password,
        confirm_new_password=data.confirm_new_password
    )