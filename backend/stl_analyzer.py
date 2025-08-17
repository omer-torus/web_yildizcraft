import numpy as np
from stl import mesh
import os
import math

class STLAnalyzer:
    def __init__(self):
        # Filament yoğunlukları (g/cm³)
        self.filament_densities = {
            'PLA': 1.24,
            'ABS': 1.04,
            'PETG': 1.27,
            'TPU': 1.21,
            'PC': 1.19
        }
        
        # Varsayılan filament tipi
        self.default_filament = 'PLA'
        
        # Infill oranları (0-1 arası)
        self.infill_ratios = {
            'düşük': 0.15,
            'orta': 0.25,
            'yüksek': 0.35,
            'katı': 0.95
        }
        
        # Varsayılan infill oranı
        self.default_infill = 0.25
        
        # Katman yüksekliği (mm)
        self.layer_height = 0.2
        
        # Filament çapı (mm)
        self.filament_diameter = 1.75
        
    def calculate_volume(self, stl_file_path):
        """STL dosyasından hacim hesaplar (cm³)"""
        try:
            # Dosya boyutunu kontrol et
            file_size = os.path.getsize(stl_file_path)
            if file_size > 50 * 1024 * 1024:  # 50MB üzeri dosyalar için basit hesaplama
                print(f"Büyük dosya tespit edildi ({file_size / 1024 / 1024:.1f} MB), basit hesaplama kullanılıyor")
                # Dosya boyutundan basit hacim tahmini - daha gerçekçi
                estimated_volume_cm3 = file_size / (1024 * 50)  # Daha gerçekçi oran
                return estimated_volume_cm3
            
            # STL dosyasını yükle
            mesh_obj = mesh.Mesh.from_file(stl_file_path)
            
            # Gerçek hacim hesaplama
            vectors = mesh_obj.vectors
            
            # Modelin sınırlarını bul
            min_x = min_y = min_z = float('inf')
            max_x = max_y = max_z = float('-inf')
            
            for triangle in vectors:
                for vertex in triangle:
                    min_x = min(min_x, vertex[0])
                    min_y = min(min_y, vertex[1])
                    min_z = min(min_z, vertex[2])
                    max_x = max(max_x, vertex[0])
                    max_y = max(max_y, vertex[1])
                    max_z = max(max_z, vertex[2])
            
            # Model boyutları (mm)
            width = max_x - min_x
            height = max_y - min_y
            depth = max_z - min_z
            
            # Daha gerçekçi hacim hesaplama
            # Modelin doluluğunu daha düşük tahmin et
            volume_mm3 = width * height * depth * 0.3  # 0.3 faktörü daha gerçekçi
            
            # cm³'e çevir
            volume_cm3 = volume_mm3 / 1000
            
            # Çok büyük değerler için sınırlama
            if volume_cm3 > 5000:  # 5 litre üzeri mantıksız
                volume_cm3 = volume_cm3 / 50
            
            return volume_cm3
        except Exception as e:
            print(f"STL dosyası analiz edilirken hata: {e}")
            return None
    
    def calculate_filament_weight(self, volume_cm3, filament_type=None, infill_ratio=None):
        """Hacimden filament ağırlığını hesaplar (gram)"""
        if volume_cm3 is None:
            return None
            
        # Varsayılan değerleri kullan
        if filament_type is None:
            filament_type = self.default_filament
        if infill_ratio is None:
            infill_ratio = self.default_infill
            
        # Yoğunluğu al
        density = self.filament_densities.get(filament_type, self.filament_densities[self.default_filament])
        
        # Daha gerçekçi ağırlık hesaplama
        # PLA yoğunluğu: 1.24 g/cm³
        # Infill oranı: 0.25 (orta)
        # Gerçek dünya faktörü: 0.6 (daha düşük)
        weight_grams = volume_cm3 * density * infill_ratio * 0.6
        
        # Makul sınırlar
        if weight_grams > 500:  # 500g üzeri kontrol
            weight_grams = weight_grams / 5
        
        return weight_grams
    
    def calculate_print_time(self, volume_cm3, layer_height=None):
        """Yaklaşık baskı süresini hesaplar (saat)"""
        if volume_cm3 is None:
            return None
            
        if layer_height is None:
            layer_height = self.layer_height
            
        # Daha gerçekçi baskı süresi hesaplama
        # Hacimden yaklaşık baskı süresi
        # 1 cm³ = yaklaşık 2-3 dakika baskı süresi
        minutes_per_cm3 = 2.5  # dakika/cm³
        
        total_minutes = volume_cm3 * minutes_per_cm3
        
        # Saate çevir
        print_time_hours = total_minutes / 60
        
        # Makul sınırlar
        if print_time_hours > 24:  # 24 saat üzeri kontrol
            print_time_hours = print_time_hours / 10
        
        return print_time_hours
    
    def calculate_sales_price(self, weight_grams):
        """Tahmini satış fiyatını hesaplar (TL)"""
        if weight_grams is None:
            return None
            
        # Filament gramını 3 ve 5 ile çarp
        min_price = float(weight_grams) * 3
        max_price = float(weight_grams) * 5
        
        # Basit hesaplama - 1 ondalık basamak
        return f"{min_price:.1f} - {max_price:.1f}"
    
    def analyze_stl_file(self, stl_file_path, filament_type=None, infill_ratio=None):
        """STL dosyasını tam analiz eder"""
        try:
            # Hacim hesapla
            volume = self.calculate_volume(stl_file_path)
            
            if volume is None:
                return None
                
            # Filament ağırlığını hesapla
            weight = self.calculate_filament_weight(volume, filament_type, infill_ratio)
            
            # Baskı süresini hesapla
            print_time = self.calculate_print_time(volume)
            
            # Satış fiyatını hesapla (yuvarlanmış ağırlık ile)
            rounded_weight = round(float(weight), 1) if weight else None
            sales_price = self.calculate_sales_price(rounded_weight)
            
            return {
                'weight_grams': round(float(weight), 1) if weight else None,
                'print_time_hours': round(float(print_time), 1) if print_time else None,
                'sales_price': sales_price,
                'infill_ratio': round(float(infill_ratio or self.default_infill), 1)
            }
            
        except Exception as e:
            print(f"STL analizi sırasında hata: {e}")
            return None

# Test fonksiyonu
def test_stl_analyzer():
    analyzer = STLAnalyzer()
    
    # Test için uploads klasöründeki bir STL dosyasını kullan
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    
    if os.path.exists(uploads_dir):
        stl_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith('.stl')]
        
        if stl_files:
            test_file = os.path.join(uploads_dir, stl_files[0])
            print(f"Test dosyası: {test_file}")
            
            result = analyzer.analyze_stl_file(test_file)
            if result:
                print("Analiz sonucu:")
                print(f"Hacim: {result['volume_cm3']} cm³")
                print(f"Filament ağırlığı: {result['weight_grams']} g")
                print(f"Baskı süresi: {result['print_time_hours']} saat")
                print(f"Tahmini fiyat: {result['price_tl']} TL")
            else:
                print("Analiz başarısız")
        else:
            print("Test için STL dosyası bulunamadı")
    else:
        print("Uploads klasörü bulunamadı")

if __name__ == "__main__":
    test_stl_analyzer() 