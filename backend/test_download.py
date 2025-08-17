import requests
import os

def test_download_stl():
    """STL dosya indirme endpoint'ini test eder"""
    print("🧪 STL Dosya İndirme Testi")
    print("=" * 40)
    
    # Önce custom design'ları listele
    try:
        response = requests.get("http://localhost:8000/custom-designs/")
        if response.status_code == 200:
            custom_designs = response.json()
            print(f"📄 Toplam custom design: {len(custom_designs)}")
            
            if custom_designs:
                # İlk custom design'ı test et
                design = custom_designs[0]
                print(f"🔍 Test edilecek design:")
                print(f"   ID: {design['id']}")
                print(f"   Müşteri: {design['customer_name']}")
                print(f"   Dosya: {design['file_path']}")
                
                # Dosya indirme testi
                download_url = f"http://localhost:8000/download-stl/{design['id']}"
                print(f"\n📥 İndirme URL: {download_url}")
                
                download_response = requests.get(download_url)
                print(f"📤 İndirme yanıtı: {download_response.status_code}")
                
                if download_response.status_code == 200:
                    # Dosyayı kaydet
                    filename = design['file_path'] or 'downloaded.stl'
                    with open(filename, 'wb') as f:
                        f.write(download_response.content)
                    
                    file_size = len(download_response.content)
                    print(f"✅ Dosya başarıyla indirildi!")
                    print(f"   Dosya adı: {filename}")
                    print(f"   Dosya boyutu: {file_size} bytes")
                    
                    # Dosyayı sil
                    if os.path.exists(filename):
                        os.remove(filename)
                        print(f"🗑️ Test dosyası silindi")
                else:
                    print(f"❌ İndirme hatası: {download_response.text}")
            else:
                print("❌ Test edilecek custom design bulunamadı")
        else:
            print(f"❌ Custom design listesi alınamadı: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_download_stl() 