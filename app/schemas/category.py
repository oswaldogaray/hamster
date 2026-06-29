from pydantic import BaseModel, Field

from app.schemas.common import TimestampedResponse


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class CategoryRead(TimestampedResponse):
    id: int
    name: str
    description: str | None
