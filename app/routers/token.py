import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

load_dotenv()
SECRET_KEY = os.getenv("KEY")
ALGORITHM = "HS256"
token_expiration_time = 12
oauth_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_token(payload: dict):
    copy_of_payload = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = token_expiration_time)
    copy_of_payload.update({"exp": expire})
    token = jwt.encode(copy_of_payload, SECRET_KEY, algorithm = ALGORITHM)
    return token

def get_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
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