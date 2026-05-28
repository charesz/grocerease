"""
GrocerEase ETL Script
---------------------
Extracts data from the main `grocerease` database,
aggregates it, and loads it into `grocerease_reports`.

Run manually:
    python etl.py

Schedule nightly (Windows Task Scheduler or cron):
    0 2 * * * python /path/to/grocerease/etl.py
"""

import sys
from datetime import date, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ── Load environment ──────────────────────────────────────────────────────────
from dotenv import load_dotenv
import os

load_dotenv()

MAIN_DB_URL      = os.getenv("MAIN_DATABASE_URL")
REPORTING_DB_URL = os.getenv("REPORTING_DATABASE_URL")

if not MAIN_DB_URL or not REPORTING_DB_URL:
    print("ERROR: DATABASE URLs not found in .env")
    sys.exit(1)

# ── Engines ───────────────────────────────────────────────────────────────────
main_engine      = create_engine(MAIN_DB_URL)
reporting_engine = create_engine(REPORTING_DB_URL)

MainSession      = sessionmaker(bind=main_engine)
ReportingSession = sessionmaker(bind=reporting_engine)


# ─────────────────────────────────────────────────────────────────────────────
# EXTRACT helpers — read raw data from grocerease
# ─────────────────────────────────────────────────────────────────────────────

def extract_daily_sales(main_db, days=90):
    """One row per day for the last N days."""
    since = date.today() - timedelta(days=days)
    rows = main_db.execute(text("""
        SELECT
            DATE(o.created_at AT TIME ZONE 'Asia/Manila') AS sale_date,
            COUNT(o.id)                                   AS total_orders,
            COALESCE(SUM(o.total_amount), 0)              AS total_revenue,
            COALESCE(AVG(o.total_amount), 0)              AS avg_order_value
        FROM orders o
        WHERE o.status NOT IN ('cancelled')
          AND DATE(o.created_at AT TIME ZONE 'Asia/Manila') >= :since
        GROUP BY sale_date
        ORDER BY sale_date DESC
    """), {"since": since}).fetchall()
    return rows


def extract_product_performance(main_db):
    """Per-product totals grouped by month."""
    rows = main_db.execute(text("""
        SELECT
            p.id                                                        AS product_id,
            p.name                                                      AS product_name,
            c.name                                                      AS category_name,
            DATE_TRUNC('month', o.created_at AT TIME ZONE 'Asia/Manila')::date AS report_month,
            COALESCE(SUM(oi.quantity), 0)                               AS total_units_sold,
            COALESCE(SUM(oi.subtotal), 0)                               AS total_revenue
        FROM order_items oi
        JOIN orders  o ON oi.order_id  = o.id
        JOIN products p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        WHERE o.status NOT IN ('cancelled')
        GROUP BY p.id, p.name, c.name, report_month
        ORDER BY report_month DESC, total_revenue DESC
    """)).fetchall()
    return rows


def extract_category_revenue(main_db):
    """Revenue grouped by category per month."""
    rows = main_db.execute(text("""
        SELECT
            c.id                                                        AS category_id,
            c.name                                                      AS category_name,
            DATE_TRUNC('month', o.created_at AT TIME ZONE 'Asia/Manila')::date AS report_month,
            COALESCE(SUM(oi.subtotal), 0)                               AS total_revenue,
            COUNT(DISTINCT o.id)                                        AS total_orders
        FROM order_items oi
        JOIN orders     o ON oi.order_id  = o.id
        JOIN products   p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        WHERE o.status NOT IN ('cancelled')
        GROUP BY c.id, c.name, report_month
        ORDER BY report_month DESC, total_revenue DESC
    """)).fetchall()
    return rows


def extract_customer_stats(main_db):
    """Per-customer summary grouped by month."""
    rows = main_db.execute(text("""
        SELECT
            u.id                                                        AS user_id,
            u.full_name,
            DATE_TRUNC('month', o.created_at AT TIME ZONE 'Asia/Manila')::date AS report_month,
            COUNT(o.id)                                                 AS total_orders,
            COALESCE(SUM(o.total_amount), 0)                            AS total_spent,
            MIN(DATE(o.created_at AT TIME ZONE 'Asia/Manila'))          AS first_order_date,
            MAX(DATE(o.created_at AT TIME ZONE 'Asia/Manila'))          AS last_order_date
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.status NOT IN ('cancelled')
        GROUP BY u.id, u.full_name, report_month
        ORDER BY report_month DESC, total_spent DESC
    """)).fetchall()
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# LOAD helpers — upsert into grocerease_reports
# ─────────────────────────────────────────────────────────────────────────────

def load_daily_sales(report_db, rows):
    report_db.execute(text("DELETE FROM daily_sales"))
    for r in rows:
        report_db.execute(text("""
            INSERT INTO daily_sales (sale_date, total_orders, total_revenue, avg_order_value, etl_updated_at)
            VALUES (:sale_date, :total_orders, :total_revenue, :avg_order_value, NOW())
            ON CONFLICT (sale_date) DO UPDATE SET
                total_orders    = EXCLUDED.total_orders,
                total_revenue   = EXCLUDED.total_revenue,
                avg_order_value = EXCLUDED.avg_order_value,
                etl_updated_at  = NOW()
        """), {
            "sale_date":       r.sale_date,
            "total_orders":    r.total_orders,
            "total_revenue":   float(r.total_revenue),
            "avg_order_value": float(r.avg_order_value),
        })
    print(f"  ✓ daily_sales: {len(rows)} rows loaded")


def load_product_performance(report_db, rows):
    report_db.execute(text("DELETE FROM product_performance"))
    for r in rows:
        report_db.execute(text("""
            INSERT INTO product_performance
                (product_id, product_name, category_name, report_month, total_units_sold, total_revenue)
            VALUES
                (:product_id, :product_name, :category_name, :report_month, :total_units_sold, :total_revenue)
        """), {
            "product_id":      str(r.product_id),
            "product_name":    r.product_name,
            "category_name":   r.category_name,
            "report_month":    r.report_month,
            "total_units_sold":r.total_units_sold,
            "total_revenue":   float(r.total_revenue),
        })
    print(f"  ✓ product_performance: {len(rows)} rows loaded")


def load_category_revenue(report_db, rows):
    report_db.execute(text("DELETE FROM category_revenue"))
    for r in rows:
        report_db.execute(text("""
            INSERT INTO category_revenue
                (category_id, category_name, report_month, total_revenue, total_orders)
            VALUES
                (:category_id, :category_name, :report_month, :total_revenue, :total_orders)
        """), {
            "category_id":   r.category_id,
            "category_name": r.category_name,
            "report_month":  r.report_month,
            "total_revenue": float(r.total_revenue),
            "total_orders":  r.total_orders,
        })
    print(f"  ✓ category_revenue: {len(rows)} rows loaded")


def load_customer_stats(report_db, rows):
    report_db.execute(text("DELETE FROM customer_stats"))
    for r in rows:
        report_db.execute(text("""
            INSERT INTO customer_stats
                (user_id, full_name, report_month, total_orders, total_spent, first_order_date, last_order_date)
            VALUES
                (:user_id, :full_name, :report_month, :total_orders, :total_spent, :first_order_date, :last_order_date)
        """), {
            "user_id":          str(r.user_id),
            "full_name":        r.full_name,
            "report_month":     r.report_month,
            "total_orders":     r.total_orders,
            "total_spent":      float(r.total_spent),
            "first_order_date": r.first_order_date,
            "last_order_date":  r.last_order_date,
        })
    print(f"  ✓ customer_stats: {len(rows)} rows loaded")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run_etl():
    print(f"\n{'='*50}")
    print(f"  GrocerEase ETL — {date.today()}")
    print(f"{'='*50}")

    main_db   = MainSession()
    report_db = ReportingSession()

    try:
        print("\n[1/4] Extracting & loading daily_sales...")
        load_daily_sales(report_db, extract_daily_sales(main_db))

        print("\n[2/4] Extracting & loading product_performance...")
        load_product_performance(report_db, extract_product_performance(main_db))

        print("\n[3/4] Extracting & loading category_revenue...")
        load_category_revenue(report_db, extract_category_revenue(main_db))

        print("\n[4/4] Extracting & loading customer_stats...")
        load_customer_stats(report_db, extract_customer_stats(main_db))

        report_db.commit()
        print(f"\n{'='*50}")
        print("  ETL completed successfully!")
        print(f"{'='*50}\n")

    except Exception as e:
        report_db.rollback()
        print(f"\n ERROR: ETL failed — {e}")
        raise

    finally:
        main_db.close()
        report_db.close()


if __name__ == "__main__":
    run_etl()
