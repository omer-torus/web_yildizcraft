from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)


class UserCart(Base):
    __tablename__ = "user_carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    added_at = Column(String)  # ISO format string


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
    status = Column(String, default="Beklemede")  # Beklemede, Tamamlandı, İptal


class CustomDesign(Base):
    __tablename__ = "custom_designs"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    description = Column(String)
    file_path = Column(String, nullable=True)
    created_at = Column(String)  # ISO format string 