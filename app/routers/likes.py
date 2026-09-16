from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

from .token import get_user

router = APIRouter(
    prefix = "/likes",
    tags = ["likes"]
)

@router.post("/")
def add_like(like: schemas.Like,
         db: Session = Depends(get_db),  # noqa: B008
         current_user: models.User = Depends(get_user)):  # noqa: B008
    post = db.execute(select(models.Post).where(models.Post.id == like.post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {like.post_id} doesn't exist"
        )
    like_query = db.execute(select(models.Like).where(models.Like.post_id == like.post_id,
                models.Like.user_id == current_user.id))
    found_like = like_query.scalar_one_or_none()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "You already liked this post"
            )
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Like added successfully"}
    else:
        if not found_like:
            raise HTTPException(
                            status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Like doesn't exist"
                        )
        db.delete(found_like)
        db.commit()
        return {"message": "Like removed successfully"}