import uuid
import enum

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg

class ModeratorRole(str, enum.Enum):
    admin = "admin"
    moderator = "moderator"

class Moderator(SQLModel, table=True):
    __tablename__ = "moderators"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid"
    )
    community_uid:Optional[uuid.UUID] = Field(
        default=None, foreign_key="communities.uid"
    )
    role: ModeratorRole = Field(default=ModeratorRole.moderator)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    community:"Communities" = Relationship(back_populates="moderators")


    def __repr__(self):
        return f"<Moderator {self.uid}>"