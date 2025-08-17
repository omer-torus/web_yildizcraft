from sqlalchemy.orm import Session
from datetime import datetime
import hashlib
import os

import models
import schemas
from stl_analyzer import STLAnalyzer


# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def verify_user_password(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and user.is_active:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.password_hash == password_hash
    return False

def create_user(db: Session, user_data: schemas.UserRegister):
    # Email ve username kontrolü
    if get_user_by_email(db, user_data.email):
        return None, "Bu email adresi zaten kullanımda"
    
    if get_user_by_username(db, user_data.username):
        return None, "Bu kullanıcı adı zaten kullanımda"
    
    # Şifreyi hash'le
    password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()
    
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        full_name=user_data.full_name,
        phone=user_data.phone,
        address=user_data.address
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, None


# Cart CRUD
def get_user_cart(db: Session, user_id: int):
    cart_items = db.query(models.UserCart).filter(models.UserCart.user_id == user_id).all()
    result = []
    
    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product:
            result.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "added_at": item.added_at,
                "product_name": product.name,
                "product_price": product.price,
                "product_image_url": product.image_url
            })
    
    return result

def add_to_user_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    # Önce ürünün var olup olmadığını kontrol et
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None, "Ürün bulunamadı"
    
    # Kullanıcının sepetinde bu ürün var mı kontrol et
    existing_item = db.query(models.UserCart).filter(
        models.UserCart.user_id == user_id,
        models.UserCart.product_id == product_id
    ).first()
    
    if existing_item:
        # Miktarı güncelle
        existing_item.quantity += quantity
        db.commit()
        return existing_item, None
    else:
        # Yeni sepet öğesi ekle
        cart_item = models.UserCart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            added_at=datetime.now().isoformat()
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item, None

def update_cart_item_quantity(db: Session, user_id: int, cart_item_id: int, quantity: int):
    cart_item = db.query(models.UserCart).filter(
        models.UserCart.id == cart_item_id,
        models.UserCart.user_id == user_id
    ).first()
    
    if not cart_item:
        return None, "Sepet öğesi bulunamadı"
    
    if quantity <= 0:
        db.delete(cart_item)
        db.commit()
        return None, "Ürün sepetten kaldırıldı"
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item, None

def remove_from_user_cart(db: Session, user_id: int, cart_item_id: int):
    cart_item = db.query(models.UserCart).filter(
        models.UserCart.id == cart_item_id,
        models.UserCart.user_id == user_id
    ).first()
    
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return True
    return False

def clear_user_cart(db: Session, user_id: int):
    cart_items = db.query(models.UserCart).filter(models.UserCart.user_id == user_id).all()
    for item in cart_items:
        db.delete(item)
    db.commit()
    return True


# Admin CRUD
def get_admin_by_username(db: Session, username: str):
    return db.query(models.Admin).filter(models.Admin.username == username).first()

def verify_admin_password(db: Session, username: str, password: str):
    admin = get_admin_by_username(db, username)
    if admin and admin.is_active:
        # Basit hash kontrolü (production'da daha güvenli yöntemler kullanılmalı)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return admin.password_hash == password_hash
    return False

def create_admin(db: Session, username: str, password: str):
    # Şifreyi hash'le
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    db_admin = models.Admin(username=username, password_hash=password_hash)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


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
    try:
        print(f"CRUD: Sipariş oluşturuluyor - {order}")
        db_order = models.Order(**order.model_dump())
        print(f"CRUD: Order modeli oluşturuldu - {db_order}")
        
        # Ürün stoklarını azalt
        # order.products: '1x2,3x1' gibi (id x adet)
        print(f"CRUD: Ürün stokları güncelleniyor - {order.products}")
        for item in order.products.split(","):
            if "x" in item:
                pid, qty = item.split("x")
                try:
                    pid = int(pid)
                    qty = int(qty)
                    print(f"CRUD: Ürün {pid} stoktan {qty} adet azaltılıyor")
                except ValueError:
                    print(f"CRUD: Geçersiz ürün formatı - {item}")
                    continue
                product = db.query(models.Product).filter(models.Product.id == pid).first()
                if product and product.stock is not None:
                    product.stock = max(0, product.stock - qty)
                    print(f"CRUD: Ürün {pid} stoku {product.stock} olarak güncellendi")
        
        db.commit()
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        print(f"CRUD: Sipariş başarıyla oluşturuldu - ID: {db_order.id}")
        return db_order
    except Exception as e:
        print(f"CRUD: Sipariş oluşturma hatası - {e}")
        db.rollback()
        raise e

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None, "Sipariş bulunamadı"
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order, None

def get_user_orders(db: Session, customer_name: str, customer_phone: str):
    """Kullanıcının siparişlerini getir"""
    orders = db.query(models.Order).filter(
        models.Order.customer_name == customer_name,
        models.Order.customer_phone == customer_phone
    ).order_by(models.Order.id.desc()).all()
    return orders

# Custom Design CRUD
def get_custom_designs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CustomDesign).offset(skip).limit(limit).all()

def get_custom_design_by_id(db: Session, custom_design_id: int):
    """ID'ye göre custom design getir"""
    return db.query(models.CustomDesign).filter(models.CustomDesign.id == custom_design_id).first()

def create_custom_design(db: Session, custom_design: schemas.CustomDesignCreate):
    print(f"CRUD: Custom design oluşturuluyor - {custom_design}")
    
    # STL dosyası varsa analiz et
    if custom_design.file_path:
        uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
        stl_file_path = os.path.join(uploads_dir, custom_design.file_path)
        
        if os.path.exists(stl_file_path):
            analyzer = STLAnalyzer()
            analysis_result = analyzer.analyze_stl_file(stl_file_path)
            
            if analysis_result:
                # Analiz sonuçlarını custom design verisine ekle
                custom_design_data = custom_design.model_dump()
                custom_design_data.update({
                    'weight_grams': analysis_result['weight_grams'],
                    'print_time_hours': analysis_result['print_time_hours'],
                    'sales_price': analysis_result['sales_price'],
                    'infill_ratio': analysis_result['infill_ratio']
                })
                
                print(f"CRUD: Analiz sonuçları eklendi - {custom_design_data}")
                db_custom_design = models.CustomDesign(**custom_design_data)
            else:
                # Analiz başarısız olursa normal şekilde oluştur
                print(f"CRUD: Analiz başarısız, normal oluşturma")
                db_custom_design = models.CustomDesign(**custom_design.model_dump())
        else:
            # STL dosyası bulunamazsa normal şekilde oluştur
            print(f"CRUD: STL dosyası bulunamadı, normal oluşturma")
            db_custom_design = models.CustomDesign(**custom_design.model_dump())
    else:
        # STL dosyası yoksa normal şekilde oluştur
        print(f"CRUD: STL dosyası yok, normal oluşturma")
        db_custom_design = models.CustomDesign(**custom_design.model_dump())
    
    print(f"CRUD: Custom design modeli oluşturuldu - {db_custom_design}")
    
    db.add(db_custom_design)
    db.commit()
    db.refresh(db_custom_design)
    
    # Custom design oluşturulduktan sonra otomatik olarak sipariş oluştur
    try:
        # Sipariş verilerini hazırla
        order_data = {
            'customer_name': custom_design.customer_name,
            'customer_phone': custom_design.customer_phone,
            'customer_address': 'Özel Tasarım Talebi',
            'products': 'Özel Tasarım',  # Özel tasarım olduğunu belirt
            'total_price': 0,  # Fiyat henüz belirlenmedi
            'status': 'Beklemede',
            'order_type': 'custom_design',  # Özel tasarım olduğunu belirt
            'custom_design_id': db_custom_design.id  # Custom design ID'sini sakla
        }
        
        print(f"CRUD: Sipariş oluşturuluyor - {order_data}")
        db_order = models.Order(**order_data)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        print(f"CRUD: Sipariş başarıyla oluşturuldu - ID: {db_order.id}")
        
    except Exception as e:
        print(f"CRUD: Sipariş oluşturma hatası - {e}")
        # Sipariş oluşturulamazsa bile custom design kaydedilmiş olur
    
    print(f"CRUD: Custom design başarıyla oluşturuldu - ID: {db_custom_design.id}")
    return db_custom_design 