import requests

def test_orders():
    """Siparişleri kontrol eder"""
    print("🧪 Sipariş Kontrolü")
    print("=" * 30)
    
    try:
        # Tüm siparişleri al
        response = requests.get("http://localhost:8000/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"📄 Toplam sipariş: {len(orders)}")
            
            for order in orders:
                print(f"\n📋 Sipariş #{order['id']}")
                print(f"   Müşteri: {order['customer_name']}")
                print(f"   Telefon: {order['customer_phone']}")
                print(f"   Adres: {order['customer_address']}")
                print(f"   Ürünler: {order['products']}")
                print(f"   Durum: {order['status']}")
                print(f"   Tip: {order.get('order_type', 'normal')}")
                print(f"   Custom Design ID: {order.get('custom_design_id', 'Yok')}")
                print(f"   Toplam: {order['total_price']} TL")
        else:
            print(f"❌ Siparişler alınamadı: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_orders() 