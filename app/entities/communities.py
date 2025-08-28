from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg


class Communities(SQLModel, table=True):
    __tablename__ = "communities"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, default=uuid.uuid4, primary_key=True)
    )
    name: str = Field(unique=True, nullable=False)
    slug: str
    description: str
    creator_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    creator: Optional["User"] = Relationship(
        back_populates="communities_created", sa_relationship_kwargs={"lazy": "selectin"}
    )
    posts: List["Post"] = Relationship(
        back_populates="community", sa_relationship_kwargs={"lazy":"selectin"}
    )
    moderators: List["Moderator"] = Relationship(back_populates="community")

    def __repr__(self):
        return f"<Community - {self.name}>"
