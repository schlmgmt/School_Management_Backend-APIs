import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email SMTP Configuration
    SMTP_SERVER: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL: str = os.getenv("SMTP_USER", "")
    SENDER_PASSWORD: str = os.getenv("SMTP_PASS", "")
    
    # Password Reset Configuration
    RESET_PASSWORD_BASE_URL: str = os.getenv("RESET_PASSWORD_BASE_URL", "http://localhost:3000/reset-password")

settings = Settings()