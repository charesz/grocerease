from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
 
from app.db.session import MainBase
 
 
class CartItem(MainBase):
    __tablename__ = "cart_items"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
 
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    