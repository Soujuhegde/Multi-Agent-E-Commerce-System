from typing import List, Optional

from sqlalchemy.orm import Session

from src.database.models import (
    Product,
    Invoice,
    MarketInsight,
)


class ProductRepository:

    @staticmethod
    def get_all(
        db: Session
    ) -> List[Product]:

        return db.query(Product).all()

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int
    ) -> Optional[Product]:

        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        product_name: str
    ):

        return (
            db.query(Product)
            .filter(
                Product.product_name == product_name
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        product: Product
    ):

        db.add(product)

        db.commit()

        db.refresh(product)

        return product

    @staticmethod
    def delete(
        db: Session,
        product: Product
    ):

        db.delete(product)

        db.commit()


class InvoiceRepository:

    @staticmethod
    def create(
        db: Session,
        invoice: Invoice
    ):

        db.add(invoice)

        db.commit()

        db.refresh(invoice)

        return invoice

    @staticmethod
    def get_invoice(
        db: Session,
        invoice_number: str
    ):

        return (
            db.query(Invoice)
            .filter(
                Invoice.invoice_number ==
                invoice_number
            )
            .first()
        )


class MarketRepository:

    @staticmethod
    def create(
        db: Session,
        insight: MarketInsight
    ):

        db.add(insight)

        db.commit()

        db.refresh(insight)

        return insight

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(MarketInsight)
            .all()
        )