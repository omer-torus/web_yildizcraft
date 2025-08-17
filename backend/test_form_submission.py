import requests
import os

def test_form_submission():
    """Form gönderimini test eder"""
    base_url = "http://localhost:8000"
    
    # Test dosyası seç
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    test_file = os.path.join(uploads_dir, "anahatarlıkkkkkksonnnnnnnnnnnnnnnnn.stl")
    
    if not os.path.exists(test_file):
        print("❌ Test dosyası bulunamadı")
        return
    
    try:
        # 1. Upload testi
        print("📤 1. Dosya yükleme testi...")
        with open(test_file, 'rb') as f:
            files = {'file': ('test.stl', f, 'application/octet-stream')}
            data = {
                'name': 'Test Kullanıcı',
                'description': 'Test açıklaması'
            }
            
            response = requests.post(f"{base_url}/upload-stl/", files=files, data=data)
            print(f"   Upload yanıtı: {response.status_code}")
            upload_data = response.json()
            print(f"   Upload verisi: {upload_data}")
        
        # 2. Custom design oluşturma testi
        print("\n📝 2. Custom design oluşturma testi...")
        custom_design_data = {
            "customer_name": "Test Kullanıcı",
            "customer_phone": "5551234567",
            "description": "Test açıklaması",
            "file_path": upload_data.get('filename', 'test.stl'),
            "created_at": "2025-08-08T18:00:00.000Z"
        }
        
        print(f"   Gönderilecek veri: {custom_design_data}")
        
        response = requests.post(f"{base_url}/custom-designs/", json=custom_design_data)
        print(f"   Custom design yanıtı: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Oluşturulan kayıt: {result}")
        else:
            print(f"   Hata: {response.text}")
        
        # 3. Veritabanı kontrolü
        print("\n📊 3. Veritabanı kontrolü...")
        response = requests.get(f"{base_url}/custom-designs/")
        designs = response.json()
        
        for design in designs:
            print(f"   - ID: {design.get('id')}")
            print(f"     Müşteri: {design.get('customer_name')}")
            print(f"     Telefon: {design.get('customer_phone')}")
            print(f"     Açıklama: {design.get('description')}")
            print(f"     Dosya: {design.get('file_path')}")
            print(f"     Filament: {design.get('weight_grams')} g")
            print("     ---")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_form_submission() 