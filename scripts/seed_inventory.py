"""
Seed inventory products into SQLite database.
"""

import json

from sqlalchemy.orm import Session

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.session import SessionLocal
from src.database.models import Product


SEED_FILE = "data/inventory_seed.json"


def load_seed_data():
    with open(SEED_FILE, "r") as file:
        return json.load(file)


def seed_inventory(db: Session):

    products = load_seed_data()

    for item in products:

        exists = (
            db.query(Product)
            .filter(
                Product.product_name == item["product_name"]
            )
            .first()
        )

        if exists:
            continue

        product = Product(
            product_name=item["product_name"],
            category=item["category"],
            price=item["price"],
            stock_quantity=item["stock_quantity"]
        )

        db.add(product)

    db.commit()

    print("Inventory seeded successfully")


if __name__ == "__main__":

    db = SessionLocal()

    try:
        seed_inventory(db)

    finally:
        db.close()