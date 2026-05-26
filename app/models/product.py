import uuid
from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
 
from app.db.session import MainBase
 
 
class Product(MainBase):
    __tablename__ = "products"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_qty = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
 
 