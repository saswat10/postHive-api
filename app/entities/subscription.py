import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    community_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="communities.uid"
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Subscription {self.name}>"