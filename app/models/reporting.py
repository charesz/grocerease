from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
 
from app.db.session import ReportingBase
 
 
class DailySales(ReportingBase):
    __tablename__ = "daily_sales"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_date = Column(Date, unique=True, nullable=False, index=True)
    total_orders = Column(Integer, default=0)
    total_revenue = Column(Numeric(12, 2), default=0)
    avg_order_value = Column(Numeric(10, 2), default=0)
    etl_updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
 
 
class ProductPerformance(ReportingBase):
    __tablename__ = "product_performance"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    product_name = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    total_units_sold = Column(Integer, default=0)
    total_revenue = Column(Numeric(12, 2), default=0)
    report_month = Column(Date, nullable=False, index=True)
 
 
class CategoryRevenue(ReportingBase):
    __tablename__ = "category_revenue"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, nullable=False)
    category_name = Column(String, nullable=False)
    total_revenue = Column(Numeric(12, 2), default=0)
    total_orders = Column(Integer, default=0)
    report_month = Column(Date, nullable=False, index=True)
 
 
class CustomerStats(ReportingBase):
    __tablename__ = "customer_stats"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    full_name = Column(String, nullable=False)
    total_orders = Column(Integer, default=0)
    total_spent = Column(Numeric(12, 2), default=0)
    first_order_date = Column(Date, nullable=True)
    last_order_date = Column(Date, nullable=True)
    report_month = Column(Date, nullable=False, index=True)
    