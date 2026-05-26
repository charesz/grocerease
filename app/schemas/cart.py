from pydantic import BaseModel
from typing import Optional
from app.schemas.product import ProductOut
 
 
class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = 1
 
 
class CartItemUpdate(BaseModel):
    quantity: int
 
 
class CartItemOut(BaseModel):
    id: int
    quantity: int
    product: ProductOut
 
    class Config:
        from_attributes = True
 
 