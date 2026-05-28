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
        {
            "category_slug": "fruits-vegetables",
            "name": "Orange (1kg)",
            "description": "Sweet and tangy fresh oranges packed with vitamin C",
            "price": 79.99, "stock_qty": 110,
            "image_url": "https://i0.wp.com/cdn-prod.medicalnewstoday.com/content/images/articles/272/272782/oranges-in-a-box.jpg?w=1155&h=1444",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Pineapple (1 piece)",
            "description": "Juicy tropical pineapple with sweet and tangy flavor",
            "price": 85.00, "stock_qty": 90,
            "image_url": "https://images.everydayhealth.com/images/diet-nutrition/benefites-of-pinapple-alt1-1440x810.jpg?sfvrsn=8236cdd4_3",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Watermelon (1 whole)",
            "description": "Refreshing and hydrating large watermelon",
            "price": 120.00, "stock_qty": 60,
            "image_url": "https://snaped.fns.usda.gov/sites/default/files/styles/crop_ratio_7_5/public/seasonal-produce/2018-05/watermelon.jpg.webp?itok=4TjwcpU9",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Papaya (1 piece)",
            "description": "Soft and sweet tropical papaya fruit",
            "price": 55.00, "stock_qty": 95,
            "image_url": "https://www.dreamfoodscaribe.com/wp-content/uploads/2024/07/papaya-fruit.webp",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Pechay (1 bundle)",
            "description": "Fresh leafy green vegetable commonly used in soups",
            "price": 25.00, "stock_qty": 140,
            "image_url": "https://alliedbotanical.com/wp-content/uploads/2020/06/Anahaw.jpg",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Eggplant (1kg)",
            "description": "Fresh purple eggplants ideal for grilling and stews",
            "price": 60.00, "stock_qty": 100,
            "image_url": "https://www.bradleysmoker.com/cdn/shop/articles/Smoked-Marinated-Eggplant-Recipe-scaled.jpg?v=1675739133&width=1500",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Carrots (1kg)",
            "description": "Crunchy and sweet orange carrots rich in vitamins",
            "price": 70.00, "stock_qty": 120,
            "image_url": "https://www.trustbasket.com/cdn/shop/articles/Carrot.jpg?v=1688378789",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Bell Pepper (1kg)",
            "description": "Colorful bell peppers with sweet and mild flavor",
            "price": 95.00, "stock_qty": 85,
            "image_url": "https://healthyfamilyproject.com/wp-content/uploads/2020/05/Bell-Peppers-background.jpg",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Calamansi (500g)",
            "description": "Small Filipino citrus fruit used for cooking and drinks",
            "price": 40.00, "stock_qty": 160,
            "image_url": "https://cdn.apartmenttherapy.info/image/upload/f_auto,q_auto:eco,c_fit,w_730,h_548/stock%2Fshutterstock_2343079465",
        },
        {
            "category_slug": "fruits-vegetables",
            "name": "Sayote (1kg)",
            "description": "Mild-flavored green vegetable used in soups and stir-fries",
            "price": 35.00, "stock_qty": 130,
            "image_url": "https://greengarden.ph/cdn/shop/products/1681364383723.jpg?v=1681364458",
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
        {
            "category_slug": "dairy-eggs",
            "name": "Alaska Evaporated Milk (370ml)",
            "description": "Rich and creamy evaporated milk used for cooking and desserts",
            "price": 65.00, "stock_qty": 120,
            "image_url": "https://www.alaskamilk.com/wp-content/uploads/2017/07/New-Project-10.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Alaska Condensed Milk (390g)",
            "description": "Sweet thick milk ideal for desserts and coffee",
            "price": 75.00, "stock_qty": 110,
            "image_url": "https://www.alaskamilk.com/wp-content/uploads/2018/04/New-Project-12.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "UHT Milk (1L)",
            "description": "Long-life milk that stays fresh without refrigeration until opened",
            "price": 95.00, "stock_qty": 140,
            "image_url": "https://ever.ph/cdn/shop/files/100000008853-Selecta-Fortified-Milk-UHT-1L-2009280.jpg?v=1614307466",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Mozzarella Cheese (200g)",
            "description": "Soft and stretchy cheese perfect for pizza and pasta",
            "price": 155.00, "stock_qty": 55,
            "image_url": "https://myculturedpalate.com/wp-content/uploads/2010/01/Homemade-Mozzarella-Cheese-sliced-500x500.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Cream Cheese (250g)",
            "description": "Smooth and creamy spreadable cheese for bagels and desserts",
            "price": 145.00, "stock_qty": 65,
            "image_url": "https://www.amodernhomestead.com/wp-content/uploads/2023/11/homemade-cream-cheese-recipe-featured-500x375.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Salted Butter (250g)",
            "description": "Rich salted butter perfect for cooking and baking",
            "price": 125.00, "stock_qty": 80,
            "image_url": "https://sallysbakingaddiction.com/wp-content/uploads/2016/06/salted-vs-unsalted-butter-3.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Nestle Greek Yogurt (170g)",
            "description": "Thick high-protein yogurt with creamy texture",
            "price": 60.00, "stock_qty": 95,
            "image_url": "https://ever.ph/cdn/shop/files/100000079110-Nestle-Yogurt-Greek-Plain-110g-240430.jpg?v=1714640398",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Duck Eggs (6 pcs)",
            "description": "Large rich duck eggs ideal for baking and special dishes",
            "price": 120.00, "stock_qty": 70,
            "image_url": "https://ediblewesternny.ediblecommunities.com/wp-content/uploads/2019/06/Duck20Eggs-1024x1024.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Quail Eggs (20 pcs)",
            "description": "Small nutrient-rich eggs commonly used in Filipino dishes",
            "price": 55.00, "stock_qty": 130,
            "image_url": "https://media-cdn2.greatbritishchefs.com/media/sjoe5oid/img23534.whqc_1426x713q80.jpg",
        },
        {
            "category_slug": "dairy-eggs",
            "name": "Chocolate Milk (1L)",
            "description": "Sweet chocolate-flavored milk drink for kids and adults",
            "price": 110.00, "stock_qty": 100,
            "image_url": "https://indulge.ph/cdn/shop/files/SigChocoDrink1000ml_2048x.png?v=1683420504",
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
        {
            "category_slug": "meat-seafood",
            "name": "Pork Chop (1kg)",
            "description": "Fresh cut pork chops ideal for frying or grilling",
            "price": 239.99, "stock_qty": 65,
            "image_url": "https://justcook.butcherbox.com/wp-content/uploads/2019/06/Boneless-Porkchops-800x500.jpg",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Beef Sirloin (1kg)",
            "description": "Tender beef sirloin cuts perfect for steak or stir-fry",
            "price": 349.99, "stock_qty": 40,
            "image_url": "https://suffolkfoodhall.co.uk/wp-content/uploads/Sirloin-Steak.png",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Chicken Thighs (1kg)",
            "description": "Juicy bone-in chicken thighs for roasting or frying",
            "price": 179.99, "stock_qty": 90,
            "image_url": "https://www.hennypenny.com/wp-content/uploads/2021/05/Henny-Penny-Blog-Post-Featured-Image-Chicken-Thighs_-The-new-wings_.png",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Pork Sisig Cut (500g)",
            "description": "Chopped pork parts ideal for making sizzling sisig",
            "price": 145.00, "stock_qty": 75,
            "image_url": "https://deliciouslyrushed.com/wp-content/uploads/2024/08/Easy-Sizzling-Pork-Belly-Sisig-Recipe-with-Mayo-2.jpg",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Shrimp (500g)",
            "description": "Fresh medium-sized shrimp, cleaned and ready to cook",
            "price": 220.00, "stock_qty": 60,
            "image_url": "https://urbancowgirllife.com/wp-content/uploads/2021/10/poached-shrimp-recipe.jpg",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Squid (500g)",
            "description": "Fresh squid ideal for grilling or calamares",
            "price": 180.00, "stock_qty": 55,
            "image_url": "https://thecornishfishmonger.co.uk/cdn/shop/files/Squid_1kg_-_The_Cornish_Fishmonger_grande.jpg?v=1741011190",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Tuna Belly (500g)",
            "description": "Rich and fatty tuna belly cuts for grilling or searing",
            "price": 275.00, "stock_qty": 35,
            "image_url": "https://nghisonfoodsgroup.com/wp-content/uploads/2023/05/frozen-yellowfin-tuna-belly-nghi-son-foods-group-345.png",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Crab (1kg)",
            "description": "Fresh whole crabs for steaming or seafood dishes",
            "price": 320.00, "stock_qty": 30,
            "image_url": "https://www.tastingtable.com/img/gallery/12-tips-you-need-when-cooking-with-crab/l-intro-1667232707.jpg",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Salmon Fillet (500g)",
            "description": "Premium salmon fillet rich in omega-3 fats",
            "price": 450.00, "stock_qty": 25,
            "image_url": "https://www.fishtaseafood.com/cdn/shop/articles/Website_Blog_Banners_Salmon_600x600_crop_center.png?v=1633941669",
        },

        {
            "category_slug": "meat-seafood",
            "name": "Chicken Wings (1kg)",
            "description": "Fresh chicken wings perfect for frying or BBQ",
            "price": 199.00, "stock_qty": 85,
            "image_url": "https://www.beckandbulow.com/cdn/shop/files/chicken_wings_1200x1200.png?v=1772738103",
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
        {
            "category_slug": "beverages",
            "name": "Tanduay Rhum (1L)",
            "description": "Philippine rum known for its smooth taste and affordable price",
            "price": 81.00, "stock_qty": 120,
            "image_url": "https://www.thestreetfoodguy.com/wp-content/uploads/2025/01/photo_2025-01-26_10-45-00.jpg",
        },
        {
            "category_slug": "beverages",
            "name": "Red Horse Beer (1L)",
            "description": "Strong Filipino beer known for its high alcohol content and bold flavor",
            "price": 95.00,
            "stock_qty": 100,
            "image_url": "https://www.cebooze.com/app/uploads/2023/07/1l.jpeg",
        },
        {
            "category_slug": "beverages",
            "name": "Emperador Brandy (1L)",
            "description": "Popular Philippine brandy with a smooth and slightly sweet taste",
            "price": 120.00,
            "stock_qty": 90,
            "image_url": "https://cdn.tatlerasia.com/asiatatler/i/ph/2020/08/14151342-empy-2_cover_1285x1153.png",
        },
        {
            "category_slug": "beverages",
            "name": "San Mig Light (330ml)",
            "description": "Light Filipino beer with a crisp and refreshing taste",
            "price": 55.00,
            "stock_qty": 150,
            "image_url": "https://delivery.vikings.ph/cdn/shop/products/4.jpg?v=1599915777",
        },
        {
            "category_slug": "beverages",
            "name": "Fundador Light Brandy (1L)",
            "description": "Smooth and mellow brandy with a lighter finish",
            "price": 135.00,
            "stock_qty": 80,
            "image_url": "https://www.africaneasternonline.com/media/catalog/product/9/9/99520284_2_.png",
        },
        {
            "category_slug": "beverages",
            "name": "Smirnoff Mule (330ml)",
            "description": "Vodka-based mixed drink with a refreshing citrus ginger flavor",
            "price": 65.00,
            "stock_qty": 110,
            "image_url": "https://assets.thirst.com.ph/products/smirnoff-mule-330ml-6-pack-bottle/1_1727335939705.png",
        },
        {
            "category_slug": "beverages",
            "name": "Coca-Cola (1.5L)",
            "description": "Classic carbonated cola drink with a sweet and refreshing taste",
            "price": 75.00, "stock_qty": 200,
            "image_url": "https://shopsuki.ph/cdn/shop/files/102051426_080dc8b7-e441-4d33-8f01-2bcae3404e7d_1024x.jpg?v=1772409381",
        },
        {
            "category_slug": "beverages",
            "name": "Pepsi (1.5L)",
            "description": "Popular cola beverage with a bold and sweet flavor",
            "price": 72.00, "stock_qty": 180,
            "image_url": "https://burpcentral.com/cdn/shop/files/Pepsi1.5_2048x.jpg?v=1756883470",
        },
        {
            "category_slug": "beverages",
            "name": "RC Cola (1.5L)",
            "description": "Affordable cola drink with a smooth and sweet taste",
            "price": 55.00, "stock_qty": 160,
            "image_url": "https://foodpanda.dhmedia.io/image/darsktores-ph/food/4806527711117.jpg?height=480",
        },
        {
            "category_slug": "beverages",
            "name": "Royal Tru-Orange (1.5L)",
            "description": "Orange-flavored carbonated drink with a sweet citrus taste",
            "price": 65.00, "stock_qty": 150,
            "image_url": "https://shopmetro.ph/wp-content/uploads/2026/01/SM9083977.jpg",
        },
        {
            "category_slug": "beverages",
            "name": "Sprite (1.5L)",
            "description": "Crisp lemon-lime soda with a refreshing clean taste",
            "price": 70.00, "stock_qty": 170,
            "image_url": "https://ever.ph/cdn/shop/files/9000002367-Sprite-PET-1.5L-201120.jpg?v=1614306816",
        },
        {
            "category_slug": "beverages",
            "name": "Red Bull (250ml)",
            "description": "Energy drink that boosts alertness and physical performance",
            "price": 95.00, "stock_qty": 140,
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWHCyt-T_1SW745KpgKOWCO1pma43f4YDo7A&s",
        },
        {
            "category_slug": "beverages",
            "name": "Sting Energy Drink (330ml)",
            "description": "Affordable energy drink with a sweet and strong kick",
            "price": 35.00, "stock_qty": 220,
            "image_url": "https://primomart.ph/cdn/shop/files/4803925033551_78fc4969-3a60-4e54-b22a-75e48a76e707_512x512.jpg?v=1754894312",
        },
        {
            "category_slug": "beverages",
            "name": "Gatorade (500ml)",
            "description": "Sports drink that helps replenish electrolytes after activity",
            "price": 60.00, "stock_qty": 190,
            "image_url": "https://images.freshop.ncrcloud.com/1564405684702544330/dcfd3e51c79708de50ac6b083e638ac5_large.png",
        },
        {
            "category_slug": "beverages",
            "name": "Powerade (500ml)",
            "description": "Hydration sports drink designed for energy and recovery",
            "price": 58.00, "stock_qty": 175,
            "image_url": "https://www.cokesolutions.com/content/dam/cokesolutions/us/images/Products/POWERADE-Mountain-Berry-Blast-PET.jpg",
        },
        {
            "category_slug": "beverages",
            "name": "Monster Energy (355ml)",
            "description": "High-caffeine energy drink with a strong and bold flavor",
            "price": 120.00, "stock_qty": 130,
            "image_url": "https://valuemartgrocery.com/cdn/shop/products/MonsterEnergyDrink.png?v=1681911648",
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
        {
            "category_slug": "snacks-sweets",
            "name": "Piattos Cheese (85g)",
            "description": "Crunchy potato crisps flavored with rich and savory cheese",
            "price": 42.00,
            "stock_qty": 140,
            "image_url": "https://merkadoph.se/cdn/shop/files/piattos-cheese-85g_2.jpg?v=1705102774",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "Nova Multigrain Snacks (78g)",
            "description": "Light and crispy multigrain chips with a barbecue flavor",
            "price": 28.00,
            "stock_qty": 130,
            "image_url": "https://happyhour.ph/cdn/shop/products/nova-country-cheddar-160g-145103.jpg?v=1708591349",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "V-Cut Barbecue Chips (60g)",
            "description": "Ridged potato chips packed with smoky barbecue flavor",
            "price": 35.00,
            "stock_qty": 120,
            "image_url": "https://foodpanda.dhmedia.io/image/darkstores/nv-global-catalog/ph/79c1603e-112e-4cc5-87b2-282a63a93636.png?height=480",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "Clover Chips (85g)",
            "description": "Classic corn snacks with a crunchy texture and cheesy taste",
            "price": 30.00,
            "stock_qty": 150,
            "image_url": "https://store.iloilosupermart.com/wp-content/uploads/2020/05/45444.png",
        },
        {
            "category_slug": "snacks-sweets",
            "name": "Oishi Prawn Crackers (90g)",
            "description": "Crispy prawn-flavored crackers popular as a light snack",
            "price": 25.00,
            "stock_qty": 160,
            "image_url": "https://pinoygroseri.com/cdn/shop/products/OishiPrawnCrackersREGULAR_SMALL_2.12oz_60g_1024x.jpg?v=1650131876",
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
