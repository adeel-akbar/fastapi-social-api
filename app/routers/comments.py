from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

from .token import get_user

router = APIRouter(
    prefix = "/comments",
    tags = ["Comments"]
)

@router.post("/{id_of_post}", status_code = status.HTTP_201_CREATED,
             response_model = schemas.CommentResponse)
def create_comment(comment: schemas.Comment, id_of_post: int, db: Session = Depends(get_db),  # noqa: B008
            current_user: models.User = Depends(get_user)):  # noqa: B008
    post = db.execute(select(models.Post).where(models.Post.id == id_of_post)).scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {id_of_post} doesn't exist.."
        )
    new_comment = models.Comment(owner_id = current_user.id, 
    post_id = id_of_post, **comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}", response_model = list[schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db),  # noqa: B008
            current_user: models.User = Depends(get_user)):  # noqa: B008
    comments = db.execute(select(models.Comment).where(models.Comment.post_id == post_id)).scalars().all()
    return comments

@router.get("/single/{comment_id}", response_model = schemas.CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db),  # noqa: B008
                   current_user: models.User = Depends(get_user)):  # noqa: B008
    comment = db.execute(select(models.Comment).where(models.Comment.id == comment_id)).scalar_one_or_none()
    if not comment:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Comment with id: {comment_id} not present"
        )
    return comment

@router.delete("/{comment_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db),  # noqa: B008
                   current_user: models.User = Depends(get_user)):  # noqa: B008
    comment = db.execute(select(models.Comment).where(models.Comment.id == comment_id)).scalar_one_or_none()
    if not comment:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Comment with id: {comment_id} not present"
            )
    if comment.owner_id != current_user.id:
         raise HTTPException(
              status_code = status.HTTP_403_FORBIDDEN,
              detail = "You're unable to delete this comment because it don't belong to you"
         )
    db.delete(comment)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.patch("/{comment_id}", response_model = schemas.CommentResponse)
def update_comment(comment: schemas.Comment, comment_id: int, db: Session = Depends(get_db),  # noqa: B008
                   current_user: models.User = Depends(get_user)):  # noqa: B008
    the_comment = db.execute(select(models.Comment).where(models.Comment.id == comment_id)).scalar_one_or_none()
    if not the_comment:
                 raise HTTPException(
                     status_code = status.HTTP_404_NOT_FOUND,
                     detail = f"Comment with id: {comment_id} not present"
                 )
    if the_comment.owner_id != current_user.id:
              raise HTTPException(
                   status_code = status.HTTP_403_FORBIDDEN,
                   detail = "You're unable to update this comment because it don't belong to you"
              )
    the_comment.content = comment.content
    db.commit()
    db.refresh(the_comment)
    return the_comment