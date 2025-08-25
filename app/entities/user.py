import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    posts: List["Post"] = Relationship(back_populates="user")
    comments: List["Comments"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.name}>"
