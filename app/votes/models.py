from uuid import UUID
from pydantic import BaseModel, field_validator
from typing import Literal


class VoteModel(BaseModel):
    value: int

    @field_validator("value")
    def validate_field(cls, v):
        if v not in (-1, 0, 1):
            raise ValueError("vote must be between -1, 0 or 1")
        return v