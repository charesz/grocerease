import uuid
import enum
from sqlalchemy import Column, String, Numeric, Integer, Text, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
 
from app.db.session import MainBase
 
 
class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"
 
 
class Order(MainBase):
    __tablename__ = "orders"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    delivery_address = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
 
 
class OrderItem(MainBase):
    __tablename__ = "order_items"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
 
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    