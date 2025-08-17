import requests

def test_order_status_update():
    """Sipariş durumu değiştirme testi"""
    print("🧪 Sipariş Durumu Değiştirme Testi")
    print("=" * 40)
    
    try:
        # Önce siparişleri al
        response = requests.get("http://localhost:8000/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"📄 Toplam sipariş: {len(orders)}")
            
            if orders:
                # İlk siparişi test et
                order = orders[0]
                order_id = order['id']
                current_status = order['status']
                
                print(f"\n📋 Test edilecek sipariş:")
                print(f"   ID: {order_id}")
                print(f"   Mevcut durum: {current_status}")
                print(f"   Tip: {order.get('order_type', 'normal')}")
                
                # Durumu "Tamamlandı" olarak değiştir
                new_status = "Tamamlandı"
                print(f"\n🔄 Durum değiştiriliyor: {current_status} → {new_status}")
                
                update_response = requests.put(f"http://localhost:8000/orders/{order_id}/status?status={new_status}")
                print(f"📤 Güncelleme yanıtı: {update_response.status_code}")
                
                if update_response.status_code == 200:
                    print("✅ Durum başarıyla güncellendi!")
                    
                    # Güncellenmiş siparişi kontrol et
                    check_response = requests.get("http://localhost:8000/orders/")
                    if check_response.status_code == 200:
                        updated_orders = check_response.json()
                        updated_order = next((o for o in updated_orders if o['id'] == order_id), None)
                        if updated_order:
                            print(f"📊 Güncellenmiş durum: {updated_order['status']}")
                        else:
                            print("❌ Güncellenmiş sipariş bulunamadı")
                    else:
                        print("❌ Güncellenmiş sipariş kontrol edilemedi")
                else:
                    print(f"❌ Durum güncellenemedi: {update_response.text}")
            else:
                print("❌ Test edilecek sipariş bulunamadı")
        else:
            print(f"❌ Siparişler alınamadı: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_order_status_update() 