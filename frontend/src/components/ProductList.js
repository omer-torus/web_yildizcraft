import React, { useEffect, useState } from "react";
import axios from "axios";
import { useCart } from "../contexts/CartContext";

const CATEGORIES = [
  { key: "all", label: "Tüm Ürünler" },
  { key: "anahtarlik", label: "Anahtarlık Şablonları" },
  { key: "yedek", label: "Araba Yedek Parçaları" },
  { key: "hediyelik", label: "Hediyelik & Dekorasyon Eşyaları" },
];

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeCategory, setActiveCategory] = useState("all");
  const [addedToCart, setAddedToCart] = useState({});
  const [stockWarning, setStockWarning] = useState({});
  const { addToCart, cart } = useCart();

  const fetchProducts = (category = null) => {
    setLoading(true);
    const url = category && category !== "all" 
      ? `http://localhost:8000/products/?category=${category}`
      : "http://localhost:8000/products/";
    
    axios.get(url)
      .then(res => {
        setProducts(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError("Ürünler yüklenemedi.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  useEffect(() => {
    fetchProducts(activeCategory);
  }, [activeCategory]);

  const handleDelete = (id) => {
    axios.delete(`http://localhost:8000/products/${id}`)
      .then(() => {
        setProducts(products.filter(product => product.id !== id));
      })
      .catch(() => {
        alert("Ürün silinirken hata oluştu.");
      });
  };

  const handleAddToCart = (product) => {
    const cartItem = cart.find(item => item.id === product.id);
    if (cartItem && cartItem.quantity >= product.stock) {
      setStockWarning(prev => ({ ...prev, [product.id]: true }));
      setTimeout(() => setStockWarning(prev => ({ ...prev, [product.id]: false })), 1500);
      return;
    }
    addToCart(product);
    setAddedToCart(prev => ({ ...prev, [product.id]: true }));
    setTimeout(() => {
      setAddedToCart(prev => ({ ...prev, [product.id]: false }));
    }, 1200);
  };

  if (loading) return <div>Yükleniyor...</div>;
  if (error) return <div>{error}</div>;

  return (
    <section className="product-catalog">
      <h2>Ürün Kataloğumuz</h2>
      <p className="catalog-desc">Kaliteli 3D baskı teknolojisi ile üretilen ürünlerimizi inceleyin. Tüm siparişleriniz kapıda ödeme ile güvenle teslim edilir.</p>
      <div className="category-tabs">
        {CATEGORIES.map(cat => (
          <button
            key={cat.key}
            className={"category-tab" + (activeCategory === cat.key ? " active" : "")}
            onClick={() => setActiveCategory(cat.key)}
          >
            {cat.label}
          </button>
        ))}
      </div>
      <div className="product-list">
        {products.length === 0 ? (
          <p>Bu kategoride ürün yok.</p>
        ) : (
          products.map(product => {
            const cartItem = cart.find(item => item.id === product.id);
            const isOutOfStock = cartItem && cartItem.quantity >= product.stock;
            return (
              <div className="product-card" key={product.id}>
                <div className="product-image-wrap">
                  {product.image_url ? (
                    <img src={product.image_url} alt={product.name} className="product-image" />
                  ) : (
                    <div className="product-image-placeholder">📦</div>
                  )}
                </div>
                <div className="product-info">
                  <h3>{product.name}</h3>
                  <p className="product-desc">{product.description}</p>
                  <div className="product-price">{product.price} TL</div>
                  <div className="product-stock">Stok: {product.stock}</div>
                  <div className="product-actions">
                    <button className="add-to-cart-btn" onClick={() => handleAddToCart(product)} disabled={isOutOfStock}>
                      Sepete Ekle
                    </button>
                    {addedToCart[product.id] && <span className="added-to-cart-msg">Sepete eklendi!</span>}
                    {stockWarning[product.id] && <span className="stock-warning-msg">Stok yetersiz!</span>}
                    <button className="delete-btn" onClick={() => handleDelete(product.id)}>
                      Sil
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}

export default ProductList; 