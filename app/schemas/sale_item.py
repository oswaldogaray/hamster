from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedResponse


class SaleItemBase(BaseModel):
    sale_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    subtotal: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class SaleItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    subtotal: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class SaleItemUpdate(BaseModel):
    sale_id: int | None = Field(default=None, gt=0)
    product_id: int | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, gt=0)
    unit_price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    subtotal: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)


class SaleItemRead(TimestampedResponse):
    id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
