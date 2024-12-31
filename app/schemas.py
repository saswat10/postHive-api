from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

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


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    user: UserOut

    class Config:
        form_attributes=True

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
    post: Post
    votes: int
    upvoted: bool
    
    class Config:
        form_attributes = True

class AllPostOut(BaseModel):
    info: Metadata
    results: list[PostOut]
    class Config:
        form_attributes = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    votes_count: int
    comments_count: int
    upvoted: int

# Schema for all posts by a user
class UserPostsResponse(BaseModel):
    user_id: int
    posts_count: int
    posts: List[PostResponse]