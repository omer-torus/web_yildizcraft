import React, { useState, useEffect } from "react";
import { useCart } from "./contexts/CartContext";
import axios from "axios";

function Cart() {
  const { cart, removeFromCart, updateQuantity, clearCart, loading } = useCart();
  const [customerName, setCustomerName] = useState("");
  const [customerAddress, setCustomerAddress] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [message, setMessage] = useState("");

  // Kullanıcı bilgilerini otomatik doldur
  useEffect(() => {
    const userDataStr = localStorage.getItem("userData");
    if (userDataStr) {
      try {
        const userData = JSON.parse(userDataStr);
        setCustomerName(userData.full_name);
        setCustomerAddress(userData.address);
        setCustomerPhone(userData.phone);
      } catch (error) {
        console.error("Kullanıcı bilgileri yüklenemedi:", error);
      }
    }
  }, []);

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleOrder = async (e) => {
    e.preventDefault();
    if (cart.length === 0) return;
    
    const orderData = {
      customer_name: customerName,
      customer_address: customerAddress,
      customer_phone: customerPhone,
      total_price: total,
      products: cart.map(item => `${item.id}x${item.quantity}`).join(",")
    };
    
    console.log("Gönderilen sipariş verisi:", orderData);
    
    try {
      const response = await axios.post("http://localhost:8000/orders/", orderData);
      console.log("Sipariş başarılı:", response.data);
      setMessage("Siparişiniz başarıyla alındı!");
      clearCart();
      setCustomerName("");
      setCustomerAddress("");
      setCustomerPhone("");
    } catch (error) {
      console.error("Sipariş hatası:", error);
      console.error("Hata detayı:", error.response?.data);
      setMessage(`Sipariş gönderilirken hata oluştu: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleQuantityChange = (productId, newQuantity) => {
    updateQuantity(productId, newQuantity);
  };

  if (loading) {
    return (
      <section className="cart-page">
        <h2>Sepetim</h2>
        <div className="loading">Sepet yükleniyor...</div>
      </section>
    );
  }

  return (
    <section className="cart-page">
      <h2>Sepetim</h2>
      {cart.length === 0 ? (
        <div className="empty-cart">
          <div className="empty-cart-icon">🛒</div>
          <div className="empty-cart-text">Sepetiniz şu anda boş.</div>
        </div>
      ) : (
        <div className="cart-content">
          <ul className="cart-list">
            {cart.map(item => (
              <li key={item.id} className="cart-item">
                <div className="cart-item-info">
                  <span className="cart-item-name">{item.name}</span>
                  <div className="cart-item-controls">
                    <button 
                      className="quantity-btn"
                      onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                      disabled={item.quantity <= 1}
                    >
                      -
                    </button>
                    <span className="cart-item-qty">{item.quantity}</span>
                    <button 
                      className="quantity-btn"
                      onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                    >
                      +
                    </button>
                  </div>
                </div>
                <div className="cart-item-right">
                  <span className="cart-item-price">{item.price * item.quantity} TL</span>
                  <button className="cart-remove-btn" onClick={() => removeFromCart(item.id)}>Kaldır</button>
                </div>
              </li>
            ))}
          </ul>
          <div className="cart-total-row">
            <span>Toplam:</span>
            <span className="cart-total">{total} TL</span>
          </div>
          <form className="order-form" onSubmit={handleOrder}>
            <h3>Sipariş Bilgileri</h3>
            <input
              type="text"
              placeholder="Ad Soyad"
              value={customerName}
              onChange={e => setCustomerName(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Adres"
              value={customerAddress}
              onChange={e => setCustomerAddress(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Telefon"
              value={customerPhone}
              onChange={e => setCustomerPhone(e.target.value)}
              required
            />
            <button type="submit" className="order-btn" disabled={cart.length === 0}>Siparişi Tamamla</button>
          </form>
          {message && <div className="order-message">{message}</div>}
        </div>
      )}
    </section>
  );
}

export default Cart; 