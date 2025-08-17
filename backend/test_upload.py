import requests
import os

def test_upload():
    """Upload işlemini test eder"""
    base_url = "http://localhost:8000"
    
    # Test dosyası seç
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    test_file = os.path.join(uploads_dir, "vent.stl")
    
    if not os.path.exists(test_file):
        print("❌ Test dosyası bulunamadı")
        return
    
    try:
        # Upload testi
        with open(test_file, 'rb') as f:
            files = {'file': ('vent.stl', f, 'application/octet-stream')}
            data = {
                'name': 'Test Kullanıcı',
                'description': 'Test açıklaması'
            }
            
            response = requests.post(f"{base_url}/upload-stl/", files=files, data=data)
            
            print(f"📤 Upload yanıtı: {response.status_code}")
            print(f"📄 Yanıt: {response.json()}")
            
    except Exception as e:
        print(f"❌ Upload test hatası: {e}")

if __name__ == "__main__":
    test_upload() 