from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.core.config import settings
from app.api.endpoints import auth, products, cart, orders, reports
 
app = FastAPI(
    title=settings.APP_NAME,
    description="Food & Groceries E-Commerce API",
    version="1.0.0",
)
 
# CORS — allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Register routers
app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(products.router, prefix="/api",          tags=["Products"])
app.include_router(cart.router,     prefix="/api/cart",     tags=["Cart"])
app.include_router(orders.router,   prefix="/api/orders",   tags=["Orders"])
app.include_router(reports.router,  prefix="/api/reports",  tags=["Reports"])
 
 
@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "docs": "/docs"}
 
 