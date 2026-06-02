"""
Invoice Schemas
"""

from datetime import datetime

from pydantic import BaseModel

from typing import List


class InvoiceItemRequest(BaseModel):

    product_id: int

    quantity: int


class InvoiceCreateRequest(BaseModel):

    customer_name: str

    items: List[InvoiceItemRequest]


class InvoiceItemResponse(BaseModel):

    product_id: int

    quantity: int

    unit_price: float


class InvoiceResponse(BaseModel):

    invoice_number: str

    customer_name: str

    total_amount: float

    tax_amount: float

    created_at: datetime

    items: List[InvoiceItemResponse]