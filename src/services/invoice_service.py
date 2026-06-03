"""
Invoice Service
"""

import uuid

from sqlalchemy.orm import Session

from src.database.models import (
    Invoice,
    InvoiceItem,
    Product
)

from src.database.repository import (
    InvoiceRepository
)

from src.schemas.invoice import (
    InvoiceCreateRequest
)

from src.agents.invoice.tax_calculator import (
    TaxCalculator
)


class InvoiceService:

    @staticmethod
    def generate_invoice(
        db: Session,
        request: InvoiceCreateRequest
    ):

        subtotal = 0

        invoice_items = []

        for item in request.items:

            product = (
                db.query(Product)
                .filter(
                    Product.id ==
                    item.product_id
                )
                .first()
            )

            if not product:
                raise ValueError(
                    f"Product {item.product_id} not found"
                )

            if product.stock_quantity < item.quantity:
                raise ValueError(
                    f"Insufficient stock for product '{product.product_name}'. Available: {product.stock_quantity}, requested: {item.quantity}"
                )

            product.stock_quantity -= item.quantity

            line_total = (
                product.price *
                item.quantity
            )

            subtotal += line_total

            invoice_items.append(
                (
                    product,
                    item.quantity
                )
            )

        tax_amount = (
            TaxCalculator.calculate(
                subtotal
            )
        )

        total_amount = (
            subtotal +
            tax_amount
        )

        invoice = Invoice(
            invoice_number=
            f"INV-{uuid.uuid4().hex[:8]}",
            customer_name=
            request.customer_name,
            total_amount=
            total_amount,
            tax_amount=
            tax_amount
        )

        db.add(invoice)

        db.flush()

        for product, quantity in invoice_items:

            db_item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price
            )

            db.add(db_item)

        db.commit()

        db.refresh(invoice)

        return invoice

    @staticmethod
    def get_invoice(
        db: Session,
        invoice_number: str
    ):

        return (
            InvoiceRepository
            .get_invoice(
                db,
                invoice_number
            )
        )