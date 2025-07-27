from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    image_url = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    category = Column(String, nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_address = Column(String)
    customer_phone = Column(String)
    total_price = Column(Float)
    products = Column(String) # For simplicity, storing product IDs as a comma-separated string 