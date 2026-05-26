from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
 
 
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    address: Optional[str] = None
 
 
class UserLogin(BaseModel):
    email: EmailStr
    password: str
 
 
class UserOut(BaseModel):
    id: UUID
    email: str
    full_name: str
    address: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
 
    class Config:
        from_attributes = True
 
 
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    