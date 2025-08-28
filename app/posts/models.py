import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from ..communities.models import CommunityBase

class Post(BaseModel):
    uid: uuid.UUID
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime

    community: Optional[CommunityBase]

class PostCreateModel(BaseModel):
    title: str
    content: str
    published: bool
    community_name : str

class PostUpdateModel(BaseModel):
    title: str
    content: str
    published: bool