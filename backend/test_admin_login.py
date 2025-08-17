import requests

def test_admin_login():
    """Admin giriş testi"""
    base_url = "http://localhost:8000"
    
    try:
        print("🔐 Admin Giriş Testi")
        print("=" * 30)
        
        # Admin giriş testi
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        print(f"📤 Giriş verisi: {login_data}")
        
        response = requests.post(f"{base_url}/admin/login", json=login_data)
        print(f"📤 Giriş yanıtı: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Giriş başarılı: {result}")
        else:
            print(f"❌ Giriş hatası: {response.text}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_admin_login() 