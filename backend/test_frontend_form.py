import requests
import os

def test_frontend_form():
    """Frontend form gönderimini simüle eder"""
    base_url = "http://localhost:8000"
    
    # Test dosyası seç
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    test_file = os.path.join(uploads_dir, "anahatarlıkkkkkksonnnnnnnnnnnnnnnnn.stl")
    
    if not os.path.exists(test_file):
        print("❌ Test dosyası bulunamadı")
        return
    
    try:
        print("🧪 Frontend Form Simülasyonu")
        print("=" * 40)
        
        # 1. Dosya yükleme (frontend'teki gibi)
        print("📤 1. Dosya yükleme...")
        with open(test_file, 'rb') as f:
            form_data = {
                'name': 'Test Kullanıcı',
                'description': 'Test açıklaması',
                'file': ('test.stl', f, 'application/octet-stream')
            }
            
            response = requests.post(f"{base_url}/upload-stl/", files={'file': form_data['file']}, data={
                'name': form_data['name'],
                'description': form_data['description']
            })
            
            print(f"   Upload yanıtı: {response.status_code}")
            if response.status_code == 200:
                upload_result = response.json()
                print(f"   ✅ Upload başarılı: {upload_result['filename']}")
                print(f"   📊 Analiz: {upload_result.get('analysis', 'Yok')}")
            else:
                print(f"   ❌ Upload hatası: {response.text}")
                return
        
        # 2. Custom design oluşturma (frontend'teki gibi)
        print("\n📝 2. Custom design oluşturma...")
        custom_design_data = {
            "customer_name": "Test Kullanıcı",
            "customer_phone": "5551234567",
            "description": "Test açıklaması",
            "file_path": upload_result['filename'],
            "created_at": "2025-08-08T18:00:00.000Z"
        }
        
        print(f"   Gönderilecek veri: {custom_design_data}")
        
        response = requests.post(f"{base_url}/custom-designs/", json=custom_design_data)
        print(f"   Custom design yanıtı: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Custom design oluşturuldu: ID {result.get('id')}")
        else:
            print(f"   ❌ Custom design hatası: {response.text}")
            return
        
        # 3. Veritabanı kontrolü
        print("\n📊 3. Veritabanı kontrolü...")
        response = requests.get(f"{base_url}/custom-designs/")
        if response.status_code == 200:
            designs = response.json()
            print(f"   📄 Toplam kayıt: {len(designs)}")
            
            for design in designs:
                print(f"   - ID: {design.get('id')}")
                print(f"     Müşteri: {design.get('customer_name')}")
                print(f"     Telefon: {design.get('customer_phone')}")
                print(f"     Açıklama: {design.get('description')}")
                print(f"     Dosya: {design.get('file_path')}")
                print(f"     Filament: {design.get('weight_grams')} g")
                print("     ---")
        else:
            print(f"   ❌ Veritabanı kontrol hatası: {response.text}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_frontend_form() 