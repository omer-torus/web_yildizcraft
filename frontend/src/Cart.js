import React, { useState } from "react";
import { useCart } from "./contexts/CartContext";
import axios from "axios";

function Cart() {
  const { cart, removeFromCart, clearCart } = useCart();
  const [customerName, setCustomerName] = useState("");
  const [customerAddress, setCustomerAddress] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [message, setMessage] = useState("");

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleOrder = async (e) => {
    e.preventDefault();
    if (cart.length === 0) return;
    try {
      await axios.post("http://localhost:8000/orders/", {
        customer_name: customerName,
        customer_address: customerAddress,
        customer_phone: customerPhone,
        total_price: total,
        products: cart.map(item => `${item.id}x${item.quantity}`).join(",")
      });
      setMessage("Siparişiniz başarıyla alındı!");
      clearCart();
      setCustomerName("");
      setCustomerAddress("");
      setCustomerPhone("");
    } catch (error) {
      setMessage("Sipariş gönderilirken hata oluştu!");
    }
  };

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
                  <span className="cart-item-qty">x{item.quantity}</span>
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