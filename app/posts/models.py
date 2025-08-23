import uuid
from datetime import datetime
from pydantic import BaseModel

class Post(BaseModel):
    uid: uuid.UUID
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime

class PostCreateModel(BaseModel):
    title: str
    content: str
    published: bool

class PostUpdateModel(BaseModel):
    title: str
    content: str
    published: bool