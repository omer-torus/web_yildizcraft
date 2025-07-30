from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, status, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import json

import crud
import models
import schemas
from database import SessionLocal, engine
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the 3D Craft API"}

# User Authentication Endpoints
@app.post("/user/register")
def user_register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    user, error = crud.create_user(db, user_data)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"success": True, "user": schemas.UserResponse.from_orm(user)}

@app.post("/user/login")
def user_login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    if crud.verify_user_password(db, login_data.username, login_data.password):
        user = crud.get_user_by_username(db, login_data.username)
        return {"success": True, "user": schemas.UserResponse.from_orm(user)}
    else:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")

# Cart Endpoints
@app.get("/user/cart/{user_id}")
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = crud.get_user_cart(db, user_id)
    return {"success": True, "cart": cart_items}

@app.post("/user/cart/{user_id}/add")
def add_to_cart(user_id: int, cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    result, error = crud.add_to_user_cart(db, user_id, cart_item.product_id, cart_item.quantity)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"success": True, "message": "Ürün sepete eklendi"}

@app.put("/user/cart/{user_id}/update/{cart_item_id}")
def update_cart_item(user_id: int, cart_item_id: int, quantity: int, db: Session = Depends(get_db)):
    result, error = crud.update_cart_item_quantity(db, user_id, cart_item_id, quantity)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"success": True, "message": "Sepet güncellendi"}

@app.delete("/user/cart/{user_id}/remove/{cart_item_id}")
def remove_from_cart(user_id: int, cart_item_id: int, db: Session = Depends(get_db)):
    success = crud.remove_from_user_cart(db, user_id, cart_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    return {"success": True, "message": "Ürün sepetten kaldırıldı"}

@app.delete("/user/cart/{user_id}/clear")
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    crud.clear_user_cart(db, user_id)
    return {"success": True, "message": "Sepet temizlendi"}

# Admin Authentication Endpoints
@app.post("/admin/login")
def admin_login(login_data: schemas.AdminLogin, db: Session = Depends(get_db)):
    if crud.verify_admin_password(db, login_data.username, login_data.password):
        admin = crud.get_admin_by_username(db, login_data.username)
        return {"success": True, "admin": schemas.AdminResponse.from_orm(admin)}
    else:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")

@app.post("/admin/create")
def create_admin(login_data: schemas.AdminLogin, db: Session = Depends(get_db)):
    # İlk admin kullanıcısını oluştur (sadece bir kez çalıştırılmalı)
    existing_admin = crud.get_admin_by_username(db, login_data.username)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten mevcut")
    
    admin = crud.create_admin(db, login_data.username, login_data.password)
    return {"success": True, "admin": schemas.AdminResponse.from_orm(admin)}

# Product Endpoints
@app.post("/products/", response_model=schemas.Product)
async def create_product(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        product_data = schemas.ProductCreate(**body)
        return crud.create_product(db=db, product=product_data)
    except Exception as e:
        print(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit, category=category)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return

# Order Endpoints
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        print(f"Gelen sipariş verisi: {order}")
        result = crud.create_order(db=db, order=order)
        print(f"Sipariş başarıyla oluşturuldu: {result}")
        return result
    except Exception as e:
        print(f"Sipariş oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Sipariş oluşturulamadı: {str(e)}")

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    result, error = crud.update_order_status(db, order_id, status)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"success": True, "message": f"Sipariş durumu '{status}' olarak güncellendi"}

@app.get("/user/orders/{customer_name}/{customer_phone}")
def get_user_orders(customer_name: str, customer_phone: str, db: Session = Depends(get_db)):
    orders = crud.get_user_orders(db, customer_name, customer_phone)
    return {"success": True, "orders": orders}

# Custom Design Endpoints
@app.post("/custom-designs/", response_model=schemas.CustomDesign)
async def create_custom_design(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        custom_design_data = schemas.CustomDesignCreate(**body)
        return crud.create_custom_design(db=db, custom_design=custom_design_data)
    except Exception as e:
        print(f"Error creating custom design: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/custom-designs/", response_model=list[schemas.CustomDesign])
def read_custom_designs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    custom_designs = crud.get_custom_designs(db, skip=skip, limit=limit)
    return custom_designs

@app.post("/upload-stl/")
def upload_stl(name: str = "", description: str = "", file: UploadFile = File(...)):
    # Sadece .stl dosyası kabul et
    if not file.filename.lower().endswith(".stl"):
        raise HTTPException(status_code=400, detail="Sadece .stl dosyaları kabul edilir.")
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"message": "Dosya başarıyla yüklendi.", "filename": file.filename, "name": name, "description": description} 