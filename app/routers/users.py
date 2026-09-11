from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utilis import hash_password
from .token import get_user

router = APIRouter(
    prefix = "/users", 
    tags = ["users"]
)

@router.post(
    "/",
    response_model = schemas.UserResponse,
    status_code = status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get(
    "/",
    response_model = list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_user)
):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users