import uuid
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class UserCreateModel(BaseModel):
    name: str = Field(max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)
    
class UserModel(BaseModel):
    uid: uuid.UUID
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    created_at: datetime