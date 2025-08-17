from database import engine
import models

def recreate_database():
    """Veritabanını yeniden oluşturur"""
    try:
        print("🗄️ Veritabanı yeniden oluşturuluyor...")
        
        # Tüm tabloları sil
        models.Base.metadata.drop_all(bind=engine)
        print("✅ Eski tablolar silindi")
        
        # Yeni tabloları oluştur
        models.Base.metadata.create_all(bind=engine)
        print("✅ Yeni tablolar oluşturuldu")
        
        print("🎉 Veritabanı başarıyla yeniden oluşturuldu!")
        
    except Exception as e:
        print(f"❌ Veritabanı oluşturma hatası: {e}")

if __name__ == "__main__":
    recreate_database() 