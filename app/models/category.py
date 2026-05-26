from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
 
from app.db.session import MainBase
 
 
class Category(MainBase):
    __tablename__ = "categories"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
 
    products = relationship("Product", back_populates="category")
 
 