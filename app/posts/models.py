import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import List
from ..comments.models import ParentCommentModel

class Post(BaseModel):
    uid: uuid.UUID
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime

class PostWithCommentsModel(Post):
    comments: List[ParentCommentModel]

class PostCreateModel(BaseModel):
    title: str
    content: str
    published: bool

class PostUpdateModel(BaseModel):
    title: str
    content: str
    published: bool