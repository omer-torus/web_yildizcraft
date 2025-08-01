from pydantic import BaseModel
from typing import List, Optional

# User Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True

# Admin Schemas
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    is_active: bool = True

    class Config:
        from_attributes = True

class Admin(BaseModel):
    id: int
    username: str
    is_active: bool = True

    class Config:
        from_attributes = True

# Cart Schemas
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

# UserCart Schemas
class UserCartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    added_at: str

class UserCartCreate(UserCartBase):
    pass

class UserCart(UserCartBase):
    id: int

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock: int = 0
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    customer_name: str
    customer_address: str
    customer_phone: str
    total_price: float
    products: str
    status: str = "Beklemede"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True

# Custom Design Schemas
class CustomDesignBase(BaseModel):
    customer_name: str
    customer_phone: str
    description: str
    file_path: Optional[str] = None
    created_at: str

class CustomDesignCreate(CustomDesignBase):
    pass

class CustomDesign(CustomDesignBase):
    id: int

    class Config:
        from_attributes = True 