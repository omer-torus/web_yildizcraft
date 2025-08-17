import requests

def simple_test():
    """Basit API testi"""
    base_url = "http://localhost:8000"
    
    try:
        # Ana endpoint testi
        response = requests.get(f"{base_url}/")
        print(f"✅ Ana endpoint: {response.status_code}")
        
        # Custom designs endpoint testi
        response = requests.get(f"{base_url}/custom-designs/")
        print(f"✅ Custom designs: {response.status_code}")
        print(f"📄 Veriler: {response.json()}")
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    simple_test() 