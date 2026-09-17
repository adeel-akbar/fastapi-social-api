from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool | None = True

class Owner(BaseModel):
    email: EmailStr

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    owner_id: int
    owner: Owner

    model_config = ConfigDict(from_attributes = True)
class PostWithVote(BaseModel):
    Post: PostResponse
    likes: int
    comments: int

    model_config = ConfigDict(from_attributes = True)
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class LikeDir(IntEnum):
    down = 0
    up = 1

class Like(BaseModel):
    post_id: int
    dir: LikeDir

class Comment(BaseModel):
    content: str


class OwnerofComment(BaseModel):
    email: EmailStr

class PostComment(BaseModel):
    title: str
    content: str

class CommentResponse(Comment):
    id: int
    created_at: datetime
    owner_id: int
    post_id: int
    owner: OwnerofComment
    post: PostComment