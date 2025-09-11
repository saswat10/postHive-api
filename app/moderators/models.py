import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class ModeratorModel(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    community_uid: uuid.UUID
    role: str

class CreateModeratorModel(BaseModel):
    user_uid: uuid.UUID
    community_uid: uuid.UUID
    role: str
