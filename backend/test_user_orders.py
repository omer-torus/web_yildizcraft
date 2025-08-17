import requests

def test_user_orders():
    """Müşteri siparişlerini test eder"""
    print("🧪 Müşteri Siparişleri Testi")
    print("=" * 35)
    
    try:
        # Test müşterisi için siparişleri al
        customer_name = "Test Kullanıcı"
        customer_phone = "5551234567"
        
        response = requests.get(f"http://localhost:8000/user/orders/{customer_name}/{customer_phone}")
        if response.status_code == 200:
            data = response.json()
            orders = data.get('orders', [])
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
            print(f"❌ Müşteri siparişleri alınamadı: {response.status_code}")
            print(f"Yanıt: {response.text}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_user_orders() 