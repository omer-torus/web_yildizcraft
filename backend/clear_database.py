from sqlalchemy.orm import Session
from database import SessionLocal
import models

def clear_custom_designs():
    """Tüm custom design kayıtlarını temizler"""
    db = SessionLocal()
    try:
        # Tüm custom design kayıtlarını sil
        db.query(models.CustomDesign).delete()
        db.commit()
        print("✅ Tüm custom design kayıtları temizlendi")
    except Exception as e:
        print(f"❌ Temizleme hatası: {e}")
        db.rollback()
    finally:
        db.close()

def check_database():
    """Veritabanı durumunu kontrol eder"""
    db = SessionLocal()
    try:
        custom_designs = db.query(models.CustomDesign).all()
        print(f"📊 Veritabanında {len(custom_designs)} custom design kaydı var")
        
        for design in custom_designs:
            print(f"  - ID: {design.id}")
            print(f"    Müşteri: {design.customer_name}")
            print(f"    Telefon: {design.customer_phone}")
            print(f"    Açıklama: {design.description}")
            print(f"    Dosya: {design.file_path}")
            print(f"    Filament: {design.weight_grams} g")
            print("---")
            
    except Exception as e:
        print(f"❌ Veritabanı kontrol hatası: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🗑️ Veritabanı Temizleme")
    print("=" * 30)
    
    # Mevcut durumu kontrol et
    check_database()
    print()
    
    # Temizleme işlemi
    clear_custom_designs()
    print()
    
    # Temizlik sonrası kontrol
    check_database() 