"""
Inventory Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ProductBase(BaseModel):

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    category: str

    price: float

    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):

    product_name: Optional[str] = None

    category: Optional[str] = None

    price: Optional[float] = None

    stock_quantity: Optional[int] = None


class ProductResponse(ProductBase):

    id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class StockUpdateRequest(BaseModel):

    product_id: int

    stock_quantity: int


class InventoryCheckRequest(BaseModel):

    product_name: str


class InventoryCheckResponse(BaseModel):

    available: bool

    stock_quantity: int