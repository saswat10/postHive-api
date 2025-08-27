import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlmodel import (
    Field,
    SQLModel,
    Column,
    Enum as SqlEnum,
)
from sqlalchemy import UniqueConstraint
import sqlalchemy.dialects.postgresql as pg


class TargetType(str, Enum):
    post = "post"
    comment = "comment"


class Votes(SQLModel, table=True):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint(
        "user_uid", "target_uid", "target_type"),
    )

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    vote: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    user_uid: uuid.UUID = Field(foreign_key="users.uid", nullable=False)
    target_uid: uuid.UUID = Field(nullable=False)
    target_type: TargetType = Field(
        sa_column=Column(SqlEnum(TargetType), nullable=False)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Vote {self.uid}>"
