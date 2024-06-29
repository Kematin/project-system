from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth")


async def authenticate(secret_key: str = Depends(oauth2_scheme)) -> str:
    if not secret_key or config.BOT_SECRET_KEY != secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in for access."
        )

    return "success"
