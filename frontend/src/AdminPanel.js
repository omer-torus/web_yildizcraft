import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import ProductForm from "./ProductForm";
import "./AdminPanel.css";

function AdminPanel() {
  const [customDesigns, setCustomDesigns] = useState([]);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [activeTab, setActiveTab] = useState("custom-designs");
  const [adminUser, setAdminUser] = useState(null);
  const navigate = useNavigate();

  // Admin oturumunu storage ile güncel tut
  useEffect(() => {
    const checkAdminStatus = () => {
      const isLoggedIn = localStorage.getItem("adminLoggedIn");
      const adminData = localStorage.getItem("adminUser");
      if (!isLoggedIn || !adminData) {
        setAdminUser(null);
        navigate("/login");
        return;
      }
      try {
        setAdminUser(JSON.parse(adminData));
      } catch (error) {
        localStorage.removeItem("adminLoggedIn");
        localStorage.removeItem("adminUser");
        setAdminUser(null);
        navigate("/login");
        return;
      }
    };
    checkAdminStatus();
    const handleStorageChange = (e) => {
      if (e.key === "adminLoggedIn" || e.key === "adminUser") {
        checkAdminStatus();
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [navigate]);

  useEffect(() => {
    if (!adminUser) return;
    fetchCustomDesigns();
    fetchOrders();
    fetchProducts();
  }, [adminUser]);

  const fetchCustomDesigns = async () => {
    try {
      const response = await axios.get("http://localhost:8000/custom-designs/");
      setCustomDesigns(response.data);
    } catch (error) {
      console.error("Özel tasarım talepleri yüklenemedi:", error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await axios.get("http://localhost:8000/orders/");
      setOrders(response.data);
    } catch (error) {
      console.error("Siparişler yüklenemedi:", error);
    }
  };

  const updateOrderStatus = async (orderId, status) => {
    try {
      await axios.put(`http://localhost:8000/orders/${orderId}/status?status=${status}`);
      // Siparişleri yeniden yükle
      fetchOrders();
    } catch (error) {
      console.error("Sipariş durumu güncellenemedi:", error);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await axios.get("http://localhost:8000/products/");
      setProducts(response.data);
    } catch (error) {
      console.error("Ürünler yüklenemedi:", error);
    }
  };

  const handleProductAdded = () => {
    window.location.reload();
  };

  const handleLogout = () => {
    localStorage.removeItem("adminLoggedIn");
    localStorage.removeItem("adminUser");
    setAdminUser(null);
    navigate("/login");
  };

  const renderOrderProducts = (orderProducts) => {
    if (!orderProducts) return null;
    const items = orderProducts.split(",").map(item => {
      const [pid, qty] = item.split("x");
      const product = products.find(p => String(p.id) === String(pid));
      return product ? `${product.name} (${qty} adet)` : `ID:${pid} (${qty} adet)`;
    });
    return (
      <ul style={{ margin: 0, paddingLeft: 18 }}>
        {items.map((desc, i) => <li key={i}>{desc}</li>)}
      </ul>
    );
  };

  if (!adminUser) {
    return <div>Yükleniyor...</div>;
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>Admin Paneli</h1>
        <div className="admin-user-info">
          <span>Hoş geldiniz, {adminUser.username}</span>
          <button onClick={handleLogout} className="logout-button">
            Çıkış Yap
          </button>
        </div>
      </div>
      
      <div className="admin-tabs">
        <button 
          className={`admin-tab ${activeTab === "custom-designs" ? "active" : ""}`}
          onClick={() => setActiveTab("custom-designs")}
        >
          Özel Tasarım Talepleri ({customDesigns.length})
        </button>
        <button 
          className={`admin-tab ${activeTab === "orders" ? "active" : ""}`}
          onClick={() => setActiveTab("orders")}
        >
          Siparişler ({orders.length})
        </button>
        <button 
          className={`admin-tab ${activeTab === "add-product" ? "active" : ""}`}
          onClick={() => setActiveTab("add-product")}
        >
          Ürün Ekle
        </button>
      </div>

      <div className="admin-content">
        {activeTab === "custom-designs" && (
          <div className="custom-designs-list">
            <h2>Özel Tasarım Talepleri</h2>
            {customDesigns.length === 0 ? (
              <p>Henüz özel tasarım talebi yok.</p>
            ) : (
              customDesigns.map(design => (
                <div key={design.id} className="design-item">
                  <div className="design-header">
                    <h3>{design.customer_name}</h3>
                    <span className="design-date">{new Date(design.created_at).toLocaleDateString('tr-TR')}</span>
                  </div>
                  <p className="design-description">{design.description}</p>
                  {design.file_path && (
                    <p className="design-file">Dosya: {design.file_path}</p>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === "orders" && (
          <div className="orders-list">
            <h2>Siparişler</h2>
            {orders.length === 0 ? (
              <p>Henüz sipariş yok.</p>
            ) : (
              orders.map(order => (
                <div key={order.id} className="order-item">
                  <div className="order-header">
                    <h3>{order.customer_name}</h3>
                    <div className="order-info">
                      <span className="order-total">{order.total_price} TL</span>
                      <span className={`order-status ${order.status === 'Tamamlandı' ? 'completed' : 'pending'}`}>
                        {order.status}
                      </span>
                    </div>
                  </div>
                  <p className="order-address">{order.customer_address}</p>
                  <p className="order-phone">{order.customer_phone}</p>
                  <div className="order-products">
                    <b>Ürünler:</b>
                    {renderOrderProducts(order.products)}
                  </div>
                  {order.status !== 'Tamamlandı' && (
                    <button 
                      className="complete-order-btn"
                      onClick={() => updateOrderStatus(order.id, 'Tamamlandı')}
                    >
                      Tamamlandı Olarak İşaretle
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === "add-product" && (
          <div className="add-product-section">
            <h2>Yeni Ürün Ekle</h2>
            <ProductForm onProductAdded={handleProductAdded} />
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminPanel; 