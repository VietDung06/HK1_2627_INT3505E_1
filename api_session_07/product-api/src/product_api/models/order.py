from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db
from .product import Product

class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

class OrderItem(db.Model):
    __tablename__ = "orders_items"
    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'),
        nullable=False)

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(
        back_populates="items"
    )

    product: Mapped["Product"] = relationship()