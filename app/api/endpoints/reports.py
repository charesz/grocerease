from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
 
from app.db.session import get_reporting_db
from app.models.reporting import DailySales, ProductPerformance, CategoryRevenue, CustomerStats
from app.core.security import get_current_active_user
 
router = APIRouter()
 
 
@router.get("/daily-sales")
def get_daily_sales(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_reporting_db),
    current_user=Depends(get_current_active_user),
):
    query = db.query(DailySales).order_by(DailySales.sale_date.desc())
    if start_date:
        query = query.filter(DailySales.sale_date >= start_date)
    if end_date:
        query = query.filter(DailySales.sale_date <= end_date)
    rows = query.limit(90).all()
    return [
        {
            "sale_date": str(r.sale_date),
            "total_orders": r.total_orders,
            "total_revenue": float(r.total_revenue),
            "avg_order_value": float(r.avg_order_value),
        }
        for r in rows
    ]
 
 
@router.get("/top-products")
def get_top_products(
    month: Optional[str] = Query(None, description="YYYY-MM"),
    limit: int = Query(10),
    db: Session = Depends(get_reporting_db),
    current_user=Depends(get_current_active_user),
):
    query = db.query(ProductPerformance).order_by(ProductPerformance.total_revenue.desc())
    if month:
        query = query.filter(ProductPerformance.report_month.cast(str).like(f"{month}%"))
    rows = query.limit(limit).all()
    return [
        {
            "product_id": str(r.product_id),
            "product_name": r.product_name,
            "category_name": r.category_name,
            "total_units_sold": r.total_units_sold,
            "total_revenue": float(r.total_revenue),
        }
        for r in rows
    ]
 
 
@router.get("/category-revenue")
def get_category_revenue(
    month: Optional[str] = Query(None, description="YYYY-MM"),
    db: Session = Depends(get_reporting_db),
    current_user=Depends(get_current_active_user),
):
    query = db.query(CategoryRevenue).order_by(CategoryRevenue.total_revenue.desc())
    if month:
        query = query.filter(CategoryRevenue.report_month.cast(str).like(f"{month}%"))
    rows = query.all()
    return [
        {
            "category_name": r.category_name,
            "total_revenue": float(r.total_revenue),
            "total_orders": r.total_orders,
        }
        for r in rows
    ]
 
 
@router.get("/customers")
def get_customer_stats(
    month: Optional[str] = Query(None, description="YYYY-MM"),
    limit: int = Query(20),
    db: Session = Depends(get_reporting_db),
    current_user=Depends(get_current_active_user),
):
    query = db.query(CustomerStats).order_by(CustomerStats.total_spent.desc())
    if month:
        query = query.filter(CustomerStats.report_month.cast(str).like(f"{month}%"))
    rows = query.limit(limit).all()
    return [
        {
            "user_id": str(r.user_id),
            "full_name": r.full_name,
            "total_orders": r.total_orders,
            "total_spent": float(r.total_spent),
            "first_order_date": str(r.first_order_date) if r.first_order_date else None,
            "last_order_date": str(r.last_order_date) if r.last_order_date else None,
        }
        for r in rows
    ]

