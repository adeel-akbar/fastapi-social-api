from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

from .token import get_user

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"])

@router.post("/",
        response_model = schemas.PostResponse,
        status_code = status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(get_user)):  # noqa: B008
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/",
    response_model = list[schemas.PostWithVote])
def get_posts(
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(get_user),  # noqa: B008
    search: str = "", skip: int = 0, limit: int = 10):
    result = db.execute(select(models.Post, func.count(models.Like.user_id).label("likes")).join(models.Like, models.Post.id == models.Like.post_id, isouter = True).group_by(models.Post.id)
        .where(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip))
    posts = result.all()
    return posts

@router.get("/{post_id}",
    response_model = schemas.PostWithVote)
def get_post(post_id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(get_user)):  # noqa: B008
    post = db.execute(select(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Post.id == models.Like.post_id, isouter = True).group_by(models.Post.id)
                .where(models.Post.id == post_id)).first()
    if not post: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {post_id} not present"
        )
    return post

@router.delete("/{post_id}",
    status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(get_user)):  # noqa: B008
    post = db.execute(select(models.Post).where(models.Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {post_id} not present"
        )
    if current_user.id != post.owner_id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "This post doesn't belong to you. That's why you're unable to " \
            "delete")
    db.delete(post)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}",
    response_model = schemas.PostResponse)
def update_post(post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(get_user)):  # noqa: B008
    the_post = db.execute(select(models.Post).where(models.Post.id == post_id)).scalar_one_or_none()
    if not the_post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {post_id} not present")
    if current_user.id != the_post.owner_id:
        raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail = "This post doesn't belong to you. That's why you're unable to " \
                    "update")
    for key, value in post.model_dump().items():
        setattr(the_post, key, value)
    db.commit()
    db.refresh(the_post)
    return the_post