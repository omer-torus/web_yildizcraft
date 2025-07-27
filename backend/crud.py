from sqlalchemy.orm import Session

import models
import schemas


# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, category: str = None):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False

# Order CRUD
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.model_dump())
    # Ürün stoklarını azalt
    # order.products: '1x2,3x1' gibi (id x adet)
    for item in order.products.split(","):
        if "x" in item:
            pid, qty = item.split("x")
            try:
                pid = int(pid)
                qty = int(qty)
            except ValueError:
                continue
            product = db.query(models.Product).filter(models.Product.id == pid).first()
            if product and product.stock is not None:
                product.stock = max(0, product.stock - qty)
    db.commit()
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order 