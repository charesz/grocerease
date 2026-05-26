from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
 
from app.db.session import get_main_db
from app.models.product import Product
from app.models.category import Category
from app.models.user import User
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate, CategoryOut, CategoryCreate
from app.core.security import get_current_active_user
 
router = APIRouter()
 
 
# ── Categories ────────────────────────────────────────────────────────────────
 
@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_main_db)):
    return db.query(Category).all()
 
 
@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    cat = Category(**cat_in.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat
 
 
# ── Products ──────────────────────────────────────────────────────────────────
 
@router.get("/products", response_model=List[ProductOut])
def list_products(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_main_db),
):
    query = db.query(Product).filter(Product.is_available == True)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.all()
 
 
@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: UUID, db: Session = Depends(get_main_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
 
 
@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
 
 
@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product
 
 
@router.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_main_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Soft delete — mark unavailable instead of removing from DB
    # This preserves order history that references this product
    product.is_available = False
    product.stock_qty = 0
    db.commit()
    