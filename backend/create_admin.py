import hashlib
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def create_admin_account(username: str, password: str):
    """Admin hesabı oluşturur"""
    db = SessionLocal()
    try:
        # Şifreyi hash'le
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Admin hesabını oluştur
        admin = models.Admin(
            username=username,
            password_hash=password_hash,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print(f"✅ Admin hesabı başarıyla oluşturuldu!")
        print(f"👤 Kullanıcı adı: {username}")
        print(f"🔐 Şifre: {password}")
        print(f"🆔 Admin ID: {admin.id}")
        
        return admin
    except Exception as e:
        print(f"❌ Admin hesabı oluşturulurken hata: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def check_admin_accounts():
    """Mevcut admin hesaplarını listeler"""
    db = SessionLocal()
    try:
        admins = db.query(models.Admin).all()
        if admins:
            print("📋 Mevcut Admin Hesapları:")
            for admin in admins:
                print(f"  - ID: {admin.id}, Kullanıcı adı: {admin.username}, Aktif: {admin.is_active}")
        else:
            print("❌ Hiç admin hesabı bulunamadı!")
        return admins
    except Exception as e:
        print(f"❌ Admin hesapları kontrol edilirken hata: {e}")
        return []
    finally:
        db.close()

def test_admin_login(username: str, password: str):
    """Admin girişini test eder"""
    db = SessionLocal()
    try:
        admin = db.query(models.Admin).filter(models.Admin.username == username).first()
        if not admin:
            print(f"❌ '{username}' kullanıcı adına sahip admin bulunamadı!")
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if admin.password_hash == password_hash:
            print(f"✅ Giriş başarılı! Admin: {username}")
            return True
        else:
            print(f"❌ Şifre yanlış! Admin: {username}")
            return False
    except Exception as e:
        print(f"❌ Giriş testi sırasında hata: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Admin Hesabı Yönetimi")
    print("=" * 40)
    
    # Mevcut admin hesaplarını kontrol et
    check_admin_accounts()
    print()
    
    # Yeni admin hesabı oluştur
    username = "admin"
    password = "admin123"
    
    print(f"🆕 Yeni admin hesabı oluşturuluyor...")
    print(f"👤 Kullanıcı adı: {username}")
    print(f"🔐 Şifre: {password}")
    print()
    
    # Admin hesabını oluştur
    admin = create_admin_account(username, password)
    
    if admin:
        print()
        print("🧪 Giriş testi yapılıyor...")
        test_admin_login(username, password)
        
        print()
        print("📝 Kullanım:")
        print(f"   Kullanıcı adı: {username}")
        print(f"   Şifre: {password}")
        print("   Bu bilgilerle admin paneline giriş yapabilirsiniz.") 