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
        {
            "name": "Fruits & Vegetables",
            "slug": "fruits-vegetables",
            "description": "Fresh fruits and vegetables",
            "image_url": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400",
        },
        {
            "name": "Dairy & Eggs",
            "slug": "dairy-eggs",
            "description": "Milk, cheese, eggs and more",
            "image_url": "https://t4.ftcdn.net/jpg/00/78/39/25/360_F_78392550_0azqO8s1wBexN0q9dm1L3QbbAX6rQoPH.jpg",
        },
        {
            "name": "Meat & Seafood",
            "slug": "meat-seafood",
            "description": "Fresh meat and seafood",
            "image_url": "https://www.news-medical.net/images/news/ImageForNews_766746_17023008622003693.jpg",
        },
        {
            "name": "Beverages",
            "slug": "beverages",
            "description": "Drinks, juices and water",
            "image_url": "https://midaswellnesshub.com/wp-content/uploads/2025/12/571b3ecb0e3c4b0ab1d6723d72df48c0_1080w.jpg",
        },
        {
            "name": "Snacks & Sweets",
            "slug": "snacks-sweets",
            "description": "Chips, chocolates and snacks",
            "image_url": "https://www.foodanddrinktechnology.com/wp-content/uploads/sweets_snacks.jpg",
        },
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
            # Update image_url even if category already exists
            existing.image_url = cat_data["image_url"]
            categories[cat_data["slug"]] = existing
            print(f"  – Category '{cat_data['name']}' already exists, updating image.")
 
    db.flush()
 
    # ── Products ──────────────────────────────────────────────────────────────
    products_data = [
        # Fruits & Vegetables
        {
            "category_slug": "fruits-vegetables",
            "name": "Fresh Banana",
            "description": "Sweet and ripe Cavendish bananas",
            "price": 29.99, "stock_qty": 200,
            "image_url": "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Red Apple",
            "description": "Crisp and juicy red apples",
            "price": 49.99, "stock_qty": 150,
            "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Mango (Carabao)",
            "description": "Sweet Philippine carabao mangoes",
            "price": 59.99, "stock_qty": 100,
            "image_url": "https://lunti.ph/cdn/shop/products/50091274_510074259400294_1726967235454435328_o_530x@2x.jpg?v=1570383347",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "White Onion (1kg)",
            "description": "Fresh white onions per kilo",
            "price": 89.99, "stock_qty": 120,
            "image_url": "https://images.unsplash.com/photo-1580201092675-a0a6a6cafbb1?w=400",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Tomato (1kg)",
            "description": "Fresh ripe tomatoes per kilo",
            "price": 49.99, "stock_qty": 130,
            "image_url": "https://images-prod.healthline.com/hlcmsresource/images/AN_images/tomatoes-1296x728-feature.jpg",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Garlic (250g)",
            "description": "Fresh garlic bulbs",
            "price": 39.99, "stock_qty": 180,
            "image_url": "https://islandhealth.org/wp-content/uploads/2025/03/blog-size-graphics-1024x683.jpg",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Cabbage (1 head)",
            "description": "Fresh green cabbage",
            "price": 45.00, "stock_qty": 80,
            "image_url": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400",
        },

        # Dairy & Eggs
        {
            "category_slug": "dairy-eggs",
            "name": "Fresh Milk (1L)",
            "description": "Full cream fresh milk 1 liter",
            "price": 89.99, "stock_qty": 100,
            "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Eggs (1 dozen)",
            "description": "Farm fresh large eggs, 12 pieces",
            "price": 99.99, "stock_qty": 150,
            "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Cheddar Cheese (200g)",
            "description": "Mild cheddar cheese block",
            "price": 129.99, "stock_qty": 60,
            "image_url": "https://myfermentedfoods.com/wp-content/uploads/2020/10/Cheese-cheddar.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Butter (225g)",
            "description": "Unsalted pure cream butter",
            "price": 119.99, "stock_qty": 70,
            "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Yogurt (150g)",
            "description": "Plain creamy yogurt",
            "price": 49.99, "stock_qty": 90,
            "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400",
        },

        # Meat & Seafood
        {
            "category_slug": "meat-seafood",
            "name": "Chicken Breast (1kg)",
            "description": "Boneless skinless chicken breast",
            "price": 199.99, "stock_qty": 80,
            "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400",
        },
        {
            "category_slug": "meat-seafood",
            "name": "Pork Liempo (1kg)",
            "description": "Fresh pork belly per kilo",
            "price": 249.99, "stock_qty": 60,
            "image_url": "https://pacificbay.com.ph/cdn/shop/products/pork-belly-liempo-sliced-688862.jpg?v=1776301884&width=1000",
        },
        {
            "category_slug": "meat-seafood",
            "name": "Ground Beef (500g)",
            "description": "Lean ground beef 500 grams",
            "price": 189.99, "stock_qty": 70,
            "image_url": "https://storage.googleapis.com/grazecart-images-prod/images/99f656b4-7a21-4d42-9fb1-2c82a6156b0b.png",
        },
        {
            "category_slug": "meat-seafood",
            "name": "Tilapia (1kg)",
            "description": "Fresh whole tilapia per kilo",
            "price": 149.99, "stock_qty": 50,
            "image_url": "https://blog.suvie.com/wp-content/uploads/2021/08/tilapia-5108235_1920.jpg",
        },
        {
            "category_slug": "meat-seafood",
            "name": "Bangus (1kg)",
            "description": "Fresh milkfish per kilo",
            "price": 159.99, "stock_qty": 50,
            "image_url": "https://cdn.tasteatlas.com/images/ingredients/50bafe8df1934a449c24f8e973439249.jpg?m=facebook",
        },

        # Beverages
        {
            "category_slug": "beverages",
            "name": "Mineral Water (500ml)",
            "description": "Pure natural mineral water",
            "price": 19.99, "stock_qty": 300,
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuHwVJWn6JwZeeOmSlrquTpEnJ387s6xqQSg&s",
        },
        {
            "category_slug": "beverages",
            "name": "Orange Juice (1L)",
            "description": "100% pure squeezed orange juice",
            "price": 89.99, "stock_qty": 100,
            "image_url": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=400",
        },
        {
            "category_slug": "beverages",
            "name": "Coffee (3-in-1, 10 pcs)",
            "description": "Instant 3-in-1 coffee mix sachet pack",
            "price": 59.99, "stock_qty": 150,
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4H6FUHrdPCtDDlXL7Ax0hnJOWAhHqzjfQ8A&s",
        },
        {
            "category_slug": "beverages",
            "name": "Iced Tea (1.5L)",
            "description": "Ready to drink iced tea",
            "price": 49.99, "stock_qty": 120,
            "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400",
        },

        # Snacks & Sweets
        {
            "category_slug": "snacks-sweets",
            "name": "Potato Chips (100g)",
            "description": "Crispy salted potato chips",
            "price": 39.99, "stock_qty": 200,
            "image_url": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "Chocolate Bar (50g)",
            "description": "Creamy milk chocolate bar",
            "price": 29.99, "stock_qty": 180,
            "image_url": "https://simplyhomecooked.com/wp-content/uploads/2024/06/pistachio-chocolate-bar-dubai-chocolate-2.jpg",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "Biscuits (250g)",
            "description": "Butter biscuits in a pack",
            "price": 49.99, "stock_qty": 160,
            "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "Peanuts (200g)",
            "description": "Roasted salted peanuts",
            "price": 34.99, "stock_qty": 140,
            "image_url": "https://www.kuchpakrahahai.in/wp-content/uploads/2015/08/Air-fryer-peanuts-recipe.jpg",
        },
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
                image_url=p["image_url"],
                is_available=True,
            )
            db.add(product)
            product_count += 1
        else:
            # Update image_url even if product already exists
            existing.image_url = p["image_url"]

    db.commit()
    print(f"  ✔ {product_count} products created.")
    print("\nSeeding complete! 🎉")
    print("  Admin login  →  admin@grocerease.com  /  admin123")
 
 
if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()
