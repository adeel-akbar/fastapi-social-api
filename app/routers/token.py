from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import get_db

SECRET_KEY = settings.KEY
ALGORITHM = settings.ALGORITHM
token_expiration_time = settings.TOKEN_EXPIRY_TIME
oauth_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_token(payload: dict):
    copy_of_payload = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = token_expiration_time)
    copy_of_payload.update({"exp": expire})
    token = jwt.encode(copy_of_payload, SECRET_KEY, algorithm = ALGORITHM)
    return token

def get_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):  # noqa: B008
    user_credentials = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials", 
        headers = {"WWW-AUTHENTICATE": "Bearer"}
    )
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = decoded_token.get("data")
        if not user_id:
            raise user_credentials
    except PyJWTError:
        raise user_credentials
    user = db.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if not user:
        raise user_credentials
    return user