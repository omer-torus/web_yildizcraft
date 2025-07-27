import React, { useState } from "react";
import ProductForm from "./ProductForm";
import ProductList from "./components/ProductList";
import { CartProvider, useCart } from "./contexts/CartContext";
import CustomDesignForm from "./CustomDesignForm";
import logo from "./logo.jpeg";
import "./App.css";
import Cart from "./Cart";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function Hero() {
  return (
    <section className="hero-section">
      <h1>3D Baskı ile Hayallerinizi Gerçeğe Dönüştürün</h1>
      <p>Araba yedek parçalarından özel hediyelik eşyalara, firmalar için toplu anahtarlık üretiminden kişisel tasarımlara kadar her türlü 3D baskı ihtiyacınız için buradayız.</p>
      <div className="hero-buttons">
        <Link to="/urunler" className="hero-btn">Ürünleri İncele</Link>
        <a href="#tasarim" className="hero-btn outline">Özel Tasarım Talebi</a>
      </div>
    </section>
  );
}

function Header() {
  const { cart, getTotalPrice } = useCart();
  const totalPrice = getTotalPrice();

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
              <ProductForm onProductAdded={handleProductAdded} />
            </div>
          </>} />
          <Route path="/urunler" element={<ProductList key={refresh} />} />
          <Route path="/sepet" element={<Cart />} />
          <Route path="/iletisim" element={<div className="contact-page">İletişim bilgileri buraya gelecek.</div>} />
        </Routes>
      </Router>
    </CartProvider>
  );
}

export default App;