from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .security import decode_token
from datetime import datetime

security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(token.credentials)

        if datetime.utcnow().timestamp() > payload.get("force_exp"):
            raise HTTPException(status_code=401, detail="Session expired")

        return payload

    except:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role(roles: list):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker