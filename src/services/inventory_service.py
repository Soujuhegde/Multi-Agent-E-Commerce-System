"""
Inventory Service
"""

from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from src.database.models import Product
from src.database.repository import ProductRepository

from src.schemas.inventory import (
    ProductCreate,
    ProductUpdate
)


class InventoryService:

    @staticmethod
    def get_all_products(
        db: Session
    ) -> List[Product]:

        return ProductRepository.get_all(db)

    @staticmethod
    def get_product(
        db: Session,
        product_id: int
    ) -> Optional[Product]:

        return ProductRepository.get_by_id(
            db,
            product_id
        )

    @staticmethod
    def create_product(
        db: Session,
        product_data: ProductCreate
    ):

        product = Product(
            product_name=product_data.product_name,
            category=product_data.category,
            price=product_data.price,
            stock_quantity=product_data.stock_quantity
        )

        return ProductRepository.create(
            db,
            product
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        update_data: ProductUpdate
    ):

        product = (
            ProductRepository
            .get_by_id(
                db,
                product_id
            )
        )

        if not product:
            return None

        for key, value in (
            update_data
            .model_dump(exclude_unset=True)
            .items()
        ):
            setattr(
                product,
                key,
                value
            )

        db.commit()

        db.refresh(product)

        return product

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int
    ):

        product = (
            ProductRepository
            .get_by_id(
                db,
                product_id
            )
        )

        if not product:
            return False

        ProductRepository.delete(
            db,
            product
        )

        return True