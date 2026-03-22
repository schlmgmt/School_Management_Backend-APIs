from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    force_exp = datetime.utcnow() + timedelta(days=7)

    to_encode.update({
        "exp": expire,
        "force_exp": force_exp.timestamp()
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

def generate_password_reset_token(user_id: int, email: str):
    """Generate a password reset token valid for 24 hours"""
    expire = datetime.utcnow() + timedelta(hours=24)
    data = {
        "user_id": user_id,
        "email": email,
        "type": "password_reset",
        "exp": expire
    }
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_password_reset_token(token: str):
    """Verify password reset token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload
    except:
        return None

def generate_temp_password():
    """Generate a temporary password"""
    import secrets
    import string
    
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    temp_password = ''.join(secrets.choice(characters) for _ in range(12))
    return temp_password