import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import Column, DateTime, func

from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg


class Comments(SQLModel, table=True):
    __tablename__ = "comments"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    content: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid"
    )
    post_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="posts.uid"
    )
    parent_comment_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="comments.uid"
    )

    # Relationships
    user: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")
    replies: List["Comments"] = Relationship(
        back_populates="parent_comment",
        sa_relationship_kwargs={"cascade":"all, delete-orphan"}
    )
    parent_comment: Optional["Comments"] = Relationship(back_populates="replies", sa_relationship_kwargs={"remote_side": "Comments.uid"})

    def __repr__(self):
        preview = (self.content[:20] + "...") if self.content and len(self.content) > 20 else self.content
        if self.parent_comment_id:
            return f"<Reply {self.uid} to {self.parent_comment_id} on post {self.post_uid} by user {self.user_uid}: '{preview}'>"
        return f"<Comment {self.uid} on post {self.post_uid} by user {self.user_uid}: '{preview}'>"