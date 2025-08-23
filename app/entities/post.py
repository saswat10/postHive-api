import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    content: str
    published: bool
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


    def __repr__(self):
        return f"<Post {self.title}>"