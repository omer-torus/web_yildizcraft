import requests
import json

def test_api():
    """API endpoint'lerini test eder"""
    base_url = "http://localhost:8000"
    
    try:
        # Ana endpoint testi
        response = requests.get(f"{base_url}/")
        print(f"✅ Ana endpoint: {response.status_code}")
        print(f"📄 Yanıt: {response.json()}")
        
        # Custom designs endpoint testi
        response = requests.get(f"{base_url}/custom-designs/")
        print(f"✅ Custom designs endpoint: {response.status_code}")
        print(f"📄 Yanıt: {response.json()}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend bağlantısı kurulamadı. Backend çalışıyor mu?")
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_api() 