import React, { useState, useEffect } from "react";
import ProductForm from "./ProductForm";
import ProductList from "./components/ProductList";
import { CartProvider, useCart } from "./contexts/CartContext";
import CustomDesignForm from "./CustomDesignForm";
import logo from "./logo.jpeg";
import "./App.css";
import Cart from "./Cart";
import AdminPanel from "./AdminPanel";
import AuthPage from "./AuthPage";
import MyOrders from "./MyOrders";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";

function Hero() {
  return (
    <section className="hero-section">
      <h1>3D Baskı ile Hayallerinizi Gerçeğe Dönüştürün</h1>
      <p>Araba yedek parçalarından özel hediyelik eşyalara, firmalar için toplu anahtarlık üretiminden kişisel tasarımlara kadar her türlü 3D baskı ihtiyacınız için buradayız.</p>
      <div className="hero-buttons">
        <Link to="/urunler" className="hero-btn">Ürünleri İncele</Link>
      </div>
    </section>
  );
}

function Header() {
  const { cart, getTotalPrice, loadUserCart } = useCart();
  const totalPrice = getTotalPrice();
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const checkUserStatus = () => {
      const userLoggedIn = localStorage.getItem("userLoggedIn");
      const userDataStr = localStorage.getItem("userData");
      
      if (userLoggedIn && userDataStr) {
        try {
          const user = JSON.parse(userDataStr);
          setUserData(user);
          // Kullanıcı giriş yapmışsa sepetini yükle
          loadUserCart();
        } catch (error) {
          localStorage.removeItem("userLoggedIn");
          localStorage.removeItem("userData");
          setUserData(null);
        }
      } else {
        setUserData(null);
      }
    };

    checkUserStatus();

    // Storage değişikliklerini dinle
    const handleStorageChange = () => {
      checkUserStatus();
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [loadUserCart]);

  const handleLogout = () => {
    localStorage.removeItem("userLoggedIn");
    localStorage.removeItem("userData");
    setUserData(null);
    navigate("/");
  };

  return (
    <header className="main-header">
      <div className="header-left">
        <img src={logo} alt="YildizCraft3D" className="header-logo" />
        <div>
          <div className="brand-title">YildizCraft3D</div>
          <div className="brand-desc">3D Baskı Stüdyosu</div>
        </div>
      </div>
      <nav className="main-nav">
        <Link to="/">Ana Sayfa</Link>
        <Link to="/urunler">Ürünler</Link>
        <Link to="/iletisim">İletişim</Link>
        {userData ? (
          <div className="user-menu">
            <span className="user-name">Merhaba, {userData.full_name}</span>
            <Link to="/siparislerim" className="orders-link">Siparişlerim</Link>
            <button onClick={handleLogout} className="logout-btn">Çıkış</button>
          </div>
        ) : (
          <Link to="/giris" className="auth-link">Giriş Yap</Link>
        )}
      </nav>
      <div className="header-cart">
        <Link to="/sepet" className="cart-icon">
          🛒
          {cart.length > 0 && (
            <span className="cart-total-price">{totalPrice} TL</span>
          )}
        </Link>
      </div>
    </header>
  );
}

function App() {
  const [refresh, setRefresh] = useState(false);
  const handleProductAdded = () => setRefresh(!refresh);

  return (
    <CartProvider>
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<>
            <Hero />
            <div className="main-content">
              <CustomDesignForm />
            </div>
          </>} />
          <Route path="/urunler" element={<ProductList key={refresh} />} />
          <Route path="/sepet" element={<Cart />} />
          <Route path="/giris" element={<AuthPage />} />
          <Route path="/siparislerim" element={<MyOrders />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/iletisim" element={<div className="contact-page">İletişim bilgileri buraya gelecek.</div>} />
        </Routes>
      </Router>
    </CartProvider>
  );
}

export default App;