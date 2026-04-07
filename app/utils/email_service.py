import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings


def send_admin_onboarding_email(admin_email: str, admin_name: str, temp_password: str, reset_token: str):
    """
    Send admin onboarding email with password reset token only.
    The frontend URL is constructed from settings.
    """
    try:
        subject = "School Admin Account Created - Action Required"
        
        reset_password_link = f"{settings.RESET_PASSWORD_BASE_URL}?token={reset_token}"
        
        body = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif;">
<h2>Welcome to School Management System</h2>
<p>Dear {admin_name},</p>
<p>Your admin account has been successfully created. To get started, please set your password by clicking the link below:</p>
<p style="margin: 30px 0;">
<a href="{reset_password_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">Set Your Password</a>
</p>
<p><strong>Note:</strong> This link will expire in 24 hours. Please set your password at the earliest.</p>
<p>If you didn't create this account, please contact the Super Admin.</p>
<p>Best regards,<br/>School Management Team</p>
</body>
</html>"""
        
        message = MIMEMultipart("alternative")
        message["From"] = settings.SENDER_EMAIL
        message["To"] = admin_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "html"))
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_forgot_password_email(user_email: str, user_name: str, reset_token: str):
    """
    Send forgot password email with password reset token.
    The frontend URL is constructed from settings.
    """
    try:
        subject = "Password Reset Request"
        
        reset_password_link = f"{settings.RESET_PASSWORD_BASE_URL}?token={reset_token}"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Password Reset Request</h2>
                <p>Dear {user_name},</p>
                <p>We received a request to reset your password. Click the link below to set a new password:</p>
                
                <p style="margin: 30px 0;">
                    <a href="{reset_password_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">
                        Reset Password
                    </a>
                </p>
                
                <p><strong>Note:</strong> This link will expire in 24 hours. If you did not request a password reset, please ignore this email.</p>
                
                <p>For security reasons, do not share this link with anyone.</p>
                
                <p>Best regards,<br/>School Management Team</p>
            </body>
        </html>
        """
        
        message = MIMEMultipart()
        message["From"] = settings.SENDER_EMAIL
        message["To"] = user_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "html"))
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
