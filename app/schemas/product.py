from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
 
 
class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    image_url: Optional[str]
 
    class Config:
        from_attributes = True
 
 
class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
 
 
class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    stock_qty: int = 0
    image_url: Optional[str] = None
    is_available: bool = True
 
 
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_qty: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
 
 
class ProductOut(BaseModel):
    id: UUID
    category_id: int
    name: str
    description: Optional[str]
    price: float
    stock_qty: int
    image_url: Optional[str]
    is_available: bool
    created_at: datetime
    category: Optional[CategoryOut]
 
    class Config:
        from_attributes = True
        