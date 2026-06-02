from sqlalchemy.orm import Session

from src.database.models import Product


class InventoryTools:

    @staticmethod
    def get_product(
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