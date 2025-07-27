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
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

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