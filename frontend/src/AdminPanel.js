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
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Admin oturumunu kontrol et
  useEffect(() => {
    const checkAdminStatus = () => {
      const isLoggedIn = localStorage.getItem("adminLoggedIn");
      const adminData = localStorage.getItem("adminUser");
      
      if (!isLoggedIn || !adminData) {
        setAdminUser(null);
        setIsLoading(false);
        navigate("/giris");
        return;
      }
      
      try {
        const admin = JSON.parse(adminData);
        setAdminUser(admin);
        setIsLoading(false);
      } catch (error) {
        console.error("Admin verisi parse edilemedi:", error);
        localStorage.removeItem("adminLoggedIn");
        localStorage.removeItem("adminUser");
        setAdminUser(null);
        setIsLoading(false);
        navigate("/giris");
        return;
      }
    };

    checkAdminStatus();
  }, [navigate]);

  // Admin oturumu varsa verileri yükle
  useEffect(() => {
    if (adminUser && !isLoading) {
      fetchCustomDesigns();
      fetchOrders();
      fetchProducts();
    }
  }, [adminUser, isLoading]);

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
    navigate("/giris");
  };

  const renderOrderProducts = (orderProducts, orderType) => {
    if (!orderProducts) return null;
    
    // Özel tasarım talebi ise
    if (orderType === "custom_design") {
      return (
        <div className="custom-design-order">
          <p><strong>📋 Özel Tasarım Talebi</strong></p>
          <p>Bu sipariş özel tasarım talebidir. Müşteri özel tasarım göndermiştir.</p>
        </div>
      );
    }
    
    // Normal ürün siparişi ise
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

  // Loading durumu
  if (isLoading) {
    return <div>Yükleniyor...</div>;
  }

  // Admin oturumu yoksa
  if (!adminUser) {
    return <div>Admin oturumu gerekli...</div>;
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
          className={`admin-tab ${activeTab === "products" ? "active" : ""}`}
          onClick={() => setActiveTab("products")}
        >
          Ürünler ({products.length})
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
                  <p className="design-phone">Telefon: {design.customer_phone}</p>
                  <p className="design-description">{design.description}</p>
                  {design.file_path && (
                    <div className="design-file-section">
                      <p className="design-file">Dosya: {design.file_path}</p>
                      <button 
                        className="download-stl-btn"
                        onClick={() => handleDownloadSTL(design.id, design.file_path)}
                      >
                        📥 STL Dosyasını İndir
                      </button>
                    </div>
                  )}
                  
                  {/* Filament analiz bilgileri */}
                  {design.weight_grams && (
                    <div className="filament-analysis">
                      <h4>🔬 Filament Analizi</h4>
                      <div className="filament-grid">
                        <div className="filament-item">
                          <span className="filament-label">Filament Ağırlığı:</span>
                          <span className="filament-value">{design.weight_grams?.toFixed(1)} g</span>
                        </div>
                        <div className="filament-item">
                          <span className="filament-label">Baskı Süresi:</span>
                          <span className="filament-value">{design.print_time_hours?.toFixed(1)} saat</span>
                        </div>
                        <div className="filament-item">
                          <span className="filament-label">Tahmini Satış Fiyatı:</span>
                          <span className="filament-value">{design.sales_price} TL</span>
                        </div>
                      </div>
                    </div>
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
                    {renderOrderProducts(order.products, order.order_type)}
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

        {activeTab === "products" && (
          <div className="products-list">
            <h2>Ürünler</h2>
            {products.length === 0 ? (
              <p>Henüz ürün yok.</p>
            ) : (
              <div className="admin-products-grid">
                {products.map(product => (
                  <div key={product.id} className="admin-product-card">
                    <div className="admin-product-image">
                      {product.image_url ? (
                        <img src={product.image_url} alt={product.name} />
                      ) : (
                        <div className="product-image-placeholder">📦</div>
                      )}
                    </div>
                    <div className="admin-product-info">
                      <h3>{product.name}</h3>
                      <p>{product.description}</p>
                      <div className="admin-product-details">
                        <span className="price">{product.price} TL</span>
                        <span className="stock">Stok: {product.stock}</span>
                        <span className="category">{product.category}</span>
                      </div>
                      <div className="admin-product-actions">
                        <div className="stock-edit-section">
                          <input
                            type="number"
                            min="0"
                            defaultValue={product.stock}
                            className="stock-input"
                            placeholder="Yeni stok"
                            data-product-id={product.id}
                          />
                          <button 
                            className="update-stock-btn"
                            onClick={() => {
                              const newStock = parseInt(document.querySelector(`input[data-product-id="${product.id}"]`).value);
                              if (newStock >= 0) {
                                handleUpdateStock(product.id, newStock);
                              } else {
                                alert("Stok miktarı 0 veya daha büyük olmalıdır.");
                              }
                            }}
                          >
                            Stok Güncelle
                          </button>
                        </div>
                        <button 
                          className="delete-product-btn"
                          onClick={() => handleDeleteProduct(product.id)}
                        >
                          Ürünü Sil
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
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

  async function handleDeleteProduct(productId) {
    if (window.confirm("Bu ürünü silmek istediğinizden emin misiniz?")) {
      try {
        await axios.delete(`http://localhost:8000/products/${productId}`, {
          data: {
            admin_username: adminUser.username
          }
        });
        fetchProducts(); // Ürünleri yeniden yükle
      } catch (error) {
        console.error("Ürün silinirken hata oluştu:", error);
        if (error.response && error.response.status === 401) {
          alert("Admin yetkisi gerekli. Lütfen tekrar giriş yapın.");
          handleLogout();
        } else {
          alert("Ürün silinirken hata oluştu.");
        }
      }
    }
  }

  async function handleUpdateStock(productId, newStock) {
    try {
      await axios.put(`http://localhost:8000/products/${productId}/stock`, {
        admin_username: adminUser.username,
        stock: newStock
      });
      fetchProducts(); // Ürünleri yeniden yükle
      alert("Stok başarıyla güncellendi!");
    } catch (error) {
      console.error("Stok güncellenirken hata oluştu:", error);
      if (error.response && error.response.status === 401) {
        alert("Admin yetkisi gerekli. Lütfen tekrar giriş yapın.");
        handleLogout();
      } else {
        alert("Stok güncellenirken hata oluştu.");
      }
    }
  }

  const handleDownloadSTL = async (customDesignId, filename) => {
    try {
      const response = await fetch(`http://localhost:8000/download-stl/${customDesignId}`);
      
      if (response.ok) {
        // Dosyayı blob olarak al
        const blob = await response.blob();
        
        // Dosyayı indir
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'design.stl';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        console.log('STL dosyası başarıyla indirildi');
      } else {
        alert('Dosya indirme hatası: ' + response.statusText);
      }
    } catch (error) {
      console.error('Dosya indirme hatası:', error);
      alert('Dosya indirilirken hata oluştu.');
    }
  };
}

export default AdminPanel; 