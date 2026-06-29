from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedResponse
from app.schemas.sale_item import SaleItemCreate, SaleItemRead


class SaleCreate(BaseModel):
    reference: str = Field(min_length=1, max_length=64)
    total_amount: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    sale_items: list[SaleItemCreate] = Field(default_factory=list)


class SaleUpdate(BaseModel):
    reference: str | None = Field(default=None, min_length=1, max_length=64)
    total_amount: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)


class SaleRead(TimestampedResponse):
    id: int
    reference: str
    total_amount: Decimal
    sale_items: list[SaleItemRead] = Field(default_factory=list)
