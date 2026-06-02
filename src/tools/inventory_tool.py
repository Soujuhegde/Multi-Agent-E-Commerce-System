"""
Inventory Tool
"""

from typing import Optional

from sqlalchemy.orm import Session

from src.database.models import Product


class InventoryTool:

    @staticmethod
    def get_product(
        db: Session,
        product_name: str
    ) -> Optional[Product]:

        return (
            db.query(Product)
            .filter(
                Product.product_name ==
                product_name
            )
            .first()
        )

    @staticmethod
    def check_stock(
        db: Session,
        product_name: str
    ) -> dict:

        product = (
            InventoryTool.get_product(
                db,
                product_name
            )
        )

        if not product:

            return {
                "available": False,
                "message": "Product not found"
            }

        return {
            "available":
            product.stock_quantity > 0,

            "stock_quantity":
            product.stock_quantity,

            "price":
            product.price
        }

    @staticmethod
    def reduce_stock(
        db: Session,
        product_id: int,
        quantity: int
    ):

        product = (
            db.query(Product)
            .filter(
                Product.id ==
                product_id
            )
            .first()
        )

        if not product:
            return False

        if product.stock_quantity < quantity:
            return False

        product.stock_quantity -= quantity

        db.commit()

        return True