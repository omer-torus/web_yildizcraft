import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MyOrders.css";

function MyOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const userDataStr = localStorage.getItem("userData");
    if (userDataStr) {
      try {
        const user = JSON.parse(userDataStr);
        setUserData(user);
        fetchOrders(user.full_name, user.phone);
      } catch (error) {
        setError("Kullanıcı bilgileri yüklenemedi");
        setLoading(false);
      }
    } else {
      setError("Giriş yapmanız gerekiyor");
      setLoading(false);
    }
  }, []);

  const fetchOrders = async (customerName, customerPhone) => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/user/orders/${encodeURIComponent(customerName)}/${encodeURIComponent(customerPhone)}`);
      setOrders(response.data.orders);
    } catch (error) {
      console.error("Siparişler yüklenemedi:", error);
      setError("Siparişler yüklenirken hata oluştu");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "Beklemede":
        return "pending";
      case "Tamamlandı":
        return "completed";
      case "İptal":
        return "cancelled";
      default:
        return "pending";
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case "Beklemede":
        return "Hazırlanıyor";
      case "Tamamlandı":
        return "Tamamlandı";
      case "İptal":
        return "İptal Edildi";
      default:
        return status;
    }
  };

  const renderOrderProducts = (orderProducts, orderType) => {
    if (!orderProducts) return null;
    
    // Özel tasarım talebi ise
    if (orderType === "custom_design") {
      return (
        <div className="custom-design-order">
          <p><strong>📋 Özel Tasarım Talebi</strong></p>
          <p>Bu sipariş özel tasarım talebinizdir. Tasarımınız hazırlandığında size bilgi verilecektir.</p>
        </div>
      );
    }
    
    // Normal ürün siparişi ise
    const items = orderProducts.split(",").map(item => {
      const [pid, qty] = item.split("x");
      return `Ürün ID: ${pid} (${qty} adet)`;
    });
    return (
      <ul style={{ margin: 0, paddingLeft: 18 }}>
        {items.map((desc, i) => <li key={i}>{desc}</li>)}
      </ul>
    );
  };

  if (loading) {
    return (
      <div className="my-orders-page">
        <h2>Siparişlerim</h2>
        <div className="loading">Siparişler yükleniyor...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="my-orders-page">
        <h2>Siparişlerim</h2>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="my-orders-page">
      <h2>Siparişlerim</h2>
      {orders.length === 0 ? (
        <div className="empty-orders">
          <div className="empty-orders-icon">📦</div>
          <div className="empty-orders-text">Henüz siparişiniz bulunmuyor.</div>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map(order => (
            <div key={order.id} className="order-item">
              <div className="order-header">
                <h3>Sipariş #{order.id}</h3>
                <div className="order-info">
                  <span className="order-total">{order.total_price} TL</span>
                  <span className={`order-status ${getStatusColor(order.status)}`}>
                    {getStatusText(order.status)}
                  </span>
                </div>
              </div>
              <div className="order-details">
                <p className="order-address">
                  <strong>Adres:</strong> {order.customer_address}
                </p>
                <p className="order-phone">
                  <strong>Telefon:</strong> {order.customer_phone}
                </p>
                <div className="order-products">
                  <strong>Ürünler:</strong>
                  {renderOrderProducts(order.products, order.order_type)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MyOrders; 