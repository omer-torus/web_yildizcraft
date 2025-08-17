import requests
import os

def test_small_file():
    """Küçük dosya ile test"""
    base_url = "http://localhost:8000"
    
    # En küçük STL dosyasını seç
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    test_file = os.path.join(uploads_dir, "anahatarlıkkkkkksonnnnnnnnnnnnnnnnn.stl")
    
    if not os.path.exists(test_file):
        print("❌ Test dosyası bulunamadı")
        return
    
    try:
        print(f"📁 Test dosyası: {test_file}")
        print(f"📏 Dosya boyutu: {os.path.getsize(test_file) / 1024:.1f} KB")
        
        # Upload testi
        with open(test_file, 'rb') as f:
            files = {'file': ('test.stl', f, 'application/octet-stream')}
            data = {
                'name': 'Test Kullanıcı',
                'description': 'Test açıklaması'
            }
            
            print("📤 Upload isteği gönderiliyor...")
            response = requests.post(f"{base_url}/upload-stl/", files=files, data=data)
            
            print(f"📤 Upload yanıtı: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Başarılı: {result}")
            else:
                print(f"❌ Hata: {response.status_code}")
                print(f"📄 Yanıt: {response.text}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_small_file() 