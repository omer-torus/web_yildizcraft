import os
from stl_analyzer import STLAnalyzer

def test_all_stl_files():
    """Uploads klasöründeki tüm STL dosyalarını test eder"""
    analyzer = STLAnalyzer()
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    
    if not os.path.exists(uploads_dir):
        print("❌ Uploads klasörü bulunamadı")
        return
    
    stl_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith('.stl')]
    
    if not stl_files:
        print("❌ Test için STL dosyası bulunamadı")
        return
    
    print("🔬 Tüm STL Dosyaları Analizi")
    print("=" * 50)
    
    for stl_file in stl_files:
        file_path = os.path.join(uploads_dir, stl_file)
        file_size = os.path.getsize(file_path) / 1024  # KB
        
        print(f"\n📁 Dosya: {stl_file}")
        print(f"📏 Boyut: {file_size:.1f} KB")
        
        try:
            result = analyzer.analyze_stl_file(file_path)
            if result:
                print(f"📊 Hacim: {result['volume_cm3']:.2f} cm³")
                print(f"⚖️ Filament Ağırlığı: {result['weight_grams']:.2f} g")
                print(f"⏱️ Baskı Süresi: {result['print_time_hours']:.1f} saat")
                print(f"💰 Tahmini Fiyat: {result['price_tl']:.2f} TL")
                print(f"🔧 Filament Tipi: {result['filament_type']}")
            else:
                print("❌ Analiz başarısız")
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    test_all_stl_files() 