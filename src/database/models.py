from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    declarative_base,
    relationship,
)

Base = declarative_base()


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    stock_quantity = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_number = Column(
        String,
        unique=True,
        nullable=False
    )

    customer_name = Column(
        String,
        nullable=False
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    tax_amount = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete"
    )


class InvoiceItem(Base):

    __tablename__ = "invoice_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )


class MarketInsight(Base):

    __tablename__ = "market_insights"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_name = Column(
        String,
        nullable=False
    )

    competitor_price = Column(
        Float,
        nullable=False
    )

    trend_score = Column(
        Float,
        nullable=False
    )

    demand_score = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )