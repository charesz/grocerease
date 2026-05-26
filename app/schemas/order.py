from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from app.models.order import OrderStatus
 
 
class OrderItemOut(BaseModel):
    id: int
    product_id: UUID
    quantity: int
    unit_price: float
    subtotal: float
 
    class Config:
        from_attributes = True
 
 
class OrderCreate(BaseModel):
    delivery_address: str
 
 
class OrderStatusUpdate(BaseModel):
    status: OrderStatus
 
 
class OrderOut(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatus
    total_amount: float
    delivery_address: str
    created_at: datetime
    items: List[OrderItemOut]
 
    class Config:
        from_attributes = True