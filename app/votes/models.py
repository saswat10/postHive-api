from uuid import UUID
from pydantic import BaseModel, field_validator, Field
from typing import Literal


class VoteModel(BaseModel):
    value: int = Field(le=1, ge=-1, description="Value must be between -1, 0 or 1", decimal_places=0)

    @field_validator("value")
    def validate_field(cls, v):
        if v not in (-1, 0, 1):
            raise ValueError("vote must be between -1, 0 or 1")
        return v