from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
 
from app.db.session import get_main_db
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartItemOut
from app.core.security import get_current_active_user
 
router = APIRouter()
 
 
@router.get("", response_model=List[CartItemOut])
def get_cart(
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
 
 
@router.post("", response_model=CartItemOut, status_code=201)
def add_to_cart(
    item_in: CartItemAdd,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product or not product.is_available:
        raise HTTPException(status_code=404, detail="Product not found or unavailable")
    if product.stock_qty < item_in.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
 
    # If item already in cart, increase quantity
    existing = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == item_in.product_id
    ).first()
 
    if existing:
        existing.quantity += item_in.quantity
        db.commit()
        db.refresh(existing)
        return existing
 
    cart_item = CartItem(
        user_id=current_user.id,
        product_id=item_in.product_id,
        quantity=item_in.quantity,
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item
 
 
@router.put("/{item_id}", response_model=CartItemOut)
def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id, CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = item_in.quantity
    db.commit()
    db.refresh(item)
    return item
 
 
@router.delete("/{item_id}", status_code=204)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id, CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
 