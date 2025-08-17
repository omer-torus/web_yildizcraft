from stl_analyzer import STLAnalyzer
import os

def debug_weight_calculation():
    """Filament ağırlığı hesaplamasını debug eder"""
    analyzer = STLAnalyzer()
    
    # Test dosyası seç
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    test_file = os.path.join(uploads_dir, "anahatarlıkkkkkksonnnnnnnnnnnnnnnnn.stl")
    
    if not os.path.exists(test_file):
        print("❌ Test dosyası bulunamadı")
        return
    
    try:
        print("🔍 Filament Ağırlığı Debug")
        print("=" * 30)
        
        # Hacim hesapla
        volume = analyzer.calculate_volume(test_file)
        print(f"📊 Hesaplanan hacim: {volume} cm³")
        
        # Filament ağırlığını hesapla
        weight = analyzer.calculate_filament_weight(volume)
        print(f"⚖️ Hesaplanan filament ağırlığı: {weight} g")
        
        # Satış fiyatını hesapla
        sales_price = analyzer.calculate_sales_price(weight)
        print(f"💰 Hesaplanan satış fiyatı: {sales_price} TL")
        
        # Detaylı hesaplama
        print("\n📝 Detaylı Hesaplama:")
        print(f"   Hacim: {volume} cm³")
        print(f"   Yoğunluk (PLA): 1.24 g/cm³")
        print(f"   Infill oranı: 0.25")
        print(f"   Gerçek dünya faktörü: 0.6")
        print(f"   Hesaplama: {volume} × 1.24 × 0.25 × 0.6 = {volume * 1.24 * 0.25 * 0.6} g")
        
        # Satış fiyatı hesaplama
        min_price = weight * 3
        max_price = weight * 5
        print(f"   Minimum fiyat: {weight} × 3 = {min_price} TL")
        print(f"   Maksimum fiyat: {weight} × 5 = {max_price} TL")
        
    except Exception as e:
        print(f"❌ Debug hatası: {e}")

if __name__ == "__main__":
    debug_weight_calculation() 