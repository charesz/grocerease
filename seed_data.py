"""
Seed script — populates the database with sample grocery data.
Usage: python seed.py
"""
 
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all models
from app.models import user, category, product, order, cart  # noqa

from app.db.session import MainSessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from passlib.context import CryptContext
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = MainSessionLocal()
 
def seed():
    print("Seeding database...")
 
    # ── Admin user ────────────────────────────────────────────────────────────
    existing_admin = db.query(User).filter(User.email == "admin@grocerease.com").first()
    if not existing_admin:
        admin = User(
            email="admin@grocerease.com",
            password_hash=pwd_context.hash("admin123"),
            full_name="GrocerEase Admin",
            address="GrocerEase HQ",
            is_active=True,
            is_admin=True,
        )
        db.add(admin)
        print("  ✔ Admin user created  (email: admin@grocerease.com  password: admin123)")
    else:
        print("  – Admin user already exists, skipping.")
 
    # ── Categories ────────────────────────────────────────────────────────────
    categories_data = [
        {"name": "Fruits & Vegetables", "slug": "fruits-vegetables",  "description": "Fresh fruits and vegetables"},
        {"name": "Dairy & Eggs",        "slug": "dairy-eggs",         "description": "Milk, cheese, eggs and more"},
        {"name": "Meat & Seafood",      "slug": "meat-seafood",       "description": "Fresh meat and seafood"},
        {"name": "Beverages",           "slug": "beverages",          "description": "Drinks, juices and water"},
        {"name": "Snacks & Sweets",     "slug": "snacks-sweets",      "description": "Chips, chocolates and snacks"},
    ]
 
    categories = {}
    for cat_data in categories_data:
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if not existing:
            cat = Category(**cat_data)
            db.add(cat)
            db.flush()
            categories[cat_data["slug"]] = cat
            print(f"  ✔ Category: {cat_data['name']}")
        else:
            categories[cat_data["slug"]] = existing
            print(f"  – Category '{cat_data['name']}' already exists, skipping.")
 
    db.flush()
 
    # ── Products ──────────────────────────────────────────────────────────────
    products_data = [
        # Fruits & Vegetables
        {"category_slug": "fruits-vegetables", "name": "Fresh Banana",        "description": "Sweet and ripe Cavendish bananas",          "price": 29.99,  "stock_qty": 200},
        {"category_slug": "fruits-vegetables", "name": "Red Apple",           "description": "Crisp and juicy red apples",                "price": 49.99,  "stock_qty": 150},
        {"category_slug": "fruits-vegetables", "name": "Mango (Carabao)",     "description": "Sweet Philippine carabao mangoes",          "price": 59.99,  "stock_qty": 100},
        {"category_slug": "fruits-vegetables", "name": "White Onion (1kg)",   "description": "Fresh white onions per kilo",               "price": 89.99,  "stock_qty": 120},
        {"category_slug": "fruits-vegetables", "name": "Tomato (1kg)",        "description": "Fresh ripe tomatoes per kilo",              "price": 49.99,  "stock_qty": 130},
        {"category_slug": "fruits-vegetables", "name": "Garlic (250g)",       "description": "Fresh garlic bulbs",                        "price": 39.99,  "stock_qty": 180},
        {"category_slug": "fruits-vegetables", "name": "Cabbage (1 head)",    "description": "Fresh green cabbage",                       "price": 45.00,  "stock_qty": 80},
 
        # Dairy & Eggs
        {"category_slug": "dairy-eggs", "name": "Fresh Milk (1L)",            "description": "Full cream fresh milk 1 liter",             "price": 89.99,  "stock_qty": 100},
        {"category_slug": "dairy-eggs", "name": "Eggs (1 dozen)",             "description": "Farm fresh large eggs, 12 pieces",          "price": 99.99,  "stock_qty": 150},
        {"category_slug": "dairy-eggs", "name": "Cheddar Cheese (200g)",      "description": "Mild cheddar cheese block",                 "price": 129.99, "stock_qty": 60},
        {"category_slug": "dairy-eggs", "name": "Butter (225g)",              "description": "Unsalted pure cream butter",                "price": 119.99, "stock_qty": 70},
        {"category_slug": "dairy-eggs", "name": "Yogurt (150g)",              "description": "Plain creamy yogurt",                       "price": 49.99,  "stock_qty": 90},
 
        # Meat & Seafood
        {"category_slug": "meat-seafood", "name": "Chicken Breast (1kg)",     "description": "Boneless skinless chicken breast",          "price": 199.99, "stock_qty": 80},
        {"category_slug": "meat-seafood", "name": "Pork Liempo (1kg)",        "description": "Fresh pork belly per kilo",                 "price": 249.99, "stock_qty": 60},
        {"category_slug": "meat-seafood", "name": "Ground Beef (500g)",       "description": "Lean ground beef 500 grams",               "price": 189.99, "stock_qty": 70},
        {"category_slug": "meat-seafood", "name": "Tilapia (1kg)",            "description": "Fresh whole tilapia per kilo",              "price": 149.99, "stock_qty": 50},
        {"category_slug": "meat-seafood", "name": "Bangus (1kg)",             "description": "Fresh milkfish per kilo",                   "price": 159.99, "stock_qty": 50},
 
        # Beverages
        {"category_slug": "beverages", "name": "Mineral Water (500ml)",       "description": "Pure natural mineral water",               "price": 19.99,  "stock_qty": 300},
        {"category_slug": "beverages", "name": "Orange Juice (1L)",           "description": "100% pure squeezed orange juice",          "price": 89.99,  "stock_qty": 100},
        {"category_slug": "beverages", "name": "Coffee (3-in-1, 10 pcs)",     "description": "Instant 3-in-1 coffee mix sachet pack",    "price": 59.99,  "stock_qty": 150},
        {"category_slug": "beverages", "name": "Iced Tea (1.5L)",             "description": "Ready to drink iced tea",                  "price": 49.99,  "stock_qty": 120},
 
        # Snacks & Sweets
        {"category_slug": "snacks-sweets", "name": "Potato Chips (100g)",     "description": "Crispy salted potato chips",               "price": 39.99,  "stock_qty": 200},
        {"category_slug": "snacks-sweets", "name": "Chocolate Bar (50g)",     "description": "Creamy milk chocolate bar",                "price": 29.99,  "stock_qty": 180},
        {"category_slug": "snacks-sweets", "name": "Biscuits (250g)",         "description": "Butter biscuits in a pack",                "price": 49.99,  "stock_qty": 160},
        {"category_slug": "snacks-sweets", "name": "Peanuts (200g)",          "description": "Roasted salted peanuts",                   "price": 34.99,  "stock_qty": 140},
    ]
 
    product_count = 0
    for p in products_data:
        cat = categories.get(p["category_slug"])
        if not cat:
            continue
        existing = db.query(Product).filter(Product.name == p["name"]).first()
        if not existing:
            product = Product(
                category_id=cat.id,
                name=p["name"],
                description=p["description"],
                price=p["price"],
                stock_qty=p["stock_qty"],
                is_available=True,
            )
            db.add(product)
            product_count += 1
 
    db.commit()
    print(f"  ✔ {product_count} products created.")
    print("\nSeeding complete! 🎉")
    print("  Admin login  →  admin@grocerease.com  /  admin123")
    print("  Test login   →  test@gmail.com        /  password123")
 
 
if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()
        
