from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class CommentCreateModel(BaseModel):
    content: str

class ParentCommentModel(BaseModel):
    uid: uuid.UUID
    content: str
    user_uid: Optional[uuid.UUID]
    post_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReplyModel(ParentCommentModel):
    parent_comment_id: Optional[uuid.UUID]
