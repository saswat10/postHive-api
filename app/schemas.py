from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class Metadata(BaseModel):
    count: int
    page: int
    limit: int
    total_pages: int

class CommentCreate(BaseModel):
    content: str
    post_id: int

class CommentUpdate(BaseModel):
    content: Optional[str]

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int

    class Config:
        form_attributes=True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        form_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    comments: list[CommentResponse]



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore


class PostOut(BaseModel):
    Post: Post
    votes: int
    upvoted: bool
    
    class Config:
        form_attributes = True

class AllPostOut(BaseModel):
    info: Metadata
    results: list[PostOut]
    class Config:
        form_attributes = True