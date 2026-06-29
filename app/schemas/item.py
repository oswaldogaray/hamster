from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sku: str = Field(min_length=1, max_length=64)
    quantity: int = Field(ge=0)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    quantity: int | None = Field(default=None, ge=0)


class ItemRead(ORMModel):
    id: int
    name: str
    sku: str
    quantity: int
