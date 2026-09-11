from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..utilis import verify_password
from .token import create_token

router = APIRouter(
    tags = ["login"]
)

@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.execute(select(models.User).where(models.User.email == user.username)).scalar_one_or_none()
    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Credentials"
        )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Credentials"
        )
    token = create_token({"data": db_user.id})
    return {"token": token, "token_type": "bearer"}