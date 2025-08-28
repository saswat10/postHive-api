from pydantic import BaseModel, Field
from typing import Optional
from ..auth.models import UserModel
from datetime import datetime

class CommunityCreateModel(BaseModel):
    name: str = Field(max_length=30, min_length=3)
    description: str = Field(min_length=30)


class CommunityModel(BaseModel):
    name: str
    description: str
    slug: str
    created_at: datetime
    updated_at: datetime 
    creator: Optional[UserModel] 