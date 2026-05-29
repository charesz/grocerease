from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
 
from app.db.session import get_main_db
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.user import User
from app.schemas.order import OrderOut, OrderCreate, OrderStatusUpdate, AdminOrderOut
from app.core.security import get_current_active_user
 
router = APIRouter()
 
 
@router.post("", response_model=OrderOut, status_code=201)
def place_order(
    order_in: OrderCreate,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
 
    total = sum(item.product.price * item.quantity for item in cart_items)
 
    order = Order(
        user_id=current_user.id,
        total_amount=total,
        delivery_address=order_in.delivery_address,
    )
    db.add(order)
    db.flush()  # get order.id before committing
 
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
            subtotal=item.product.price * item.quantity,
        )
        # Deduct stock
        item.product.stock_qty -= item.quantity
        db.add(order_item)
        db.delete(item)  # clear cart
 
    db.commit()
    db.refresh(order)
    return order
 
 
@router.get("", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    return db.query(Order).filter(Order.user_id == current_user.id)\
        .order_by(Order.created_at.desc()).all()
 
 
@router.get("/admin/all", response_model=List[AdminOrderOut])
def list_all_orders(
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "delivery_address": order.delivery_address,
            "created_at": order.created_at,
            "user_name": order.user.full_name if order.user else None,
            "user_email": order.user.email if order.user else None,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "product_name": item.product.name if item.product else None,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "subtotal": float(item.subtotal),
                }
                for item in order.items
            ],
        }
        result.append(AdminOrderOut(**order_dict))
    return result
 
 
@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: UUID,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    order = db.query(Order).filter(
        Order.id == order_id, Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
 
 
@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: UUID,
    status_in: OrderStatusUpdate,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status_in.status
    db.commit()
    db.refresh(order)
    return order