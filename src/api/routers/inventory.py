from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.database.models import Product

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/products")
async def get_products(
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return products


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:

        return {
            "success": False,
            "message": "Product not found"
        }

    return product


@router.post("/add")
async def add_product(
    product_name: str,
    category: str,
    price: float,
    stock_quantity: int,
    db: Session = Depends(get_db)
):

    product = Product(
        product_name=product_name,
        category=category,
        price=price,
        stock_quantity=stock_quantity
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return {
        "success": True,
        "product_id": product.id
    }


@router.put("/update-stock/{product_id}")
async def update_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:

        return {
            "success": False
        }

    product.stock_quantity = quantity

    db.commit()

    return {
        "success": True
    }


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:

        return {
            "success": False
        }

    db.delete(product)

    db.commit()

    return {
        "success": True
    }