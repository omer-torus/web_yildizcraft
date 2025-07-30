import React, { createContext, useContext, useState, useEffect, useRef } from "react";
import axios from "axios";

const CartContext = createContext();

export function useCart() {
  return useContext(CartContext);
}

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(false);
  const prevUserId = useRef(null);

  // Kullanıcı giriş durumunu kontrol et
  const getUserData = () => {
    const userDataStr = localStorage.getItem("userData");
    if (userDataStr) {
      try {
        return JSON.parse(userDataStr);
      } catch (error) {
        console.error("Kullanıcı bilgileri yüklenemedi:", error);
        return null;
      }
    }
    return null;
  };

  // Kullanıcının sepetini yükle
  const loadUserCart = async () => {
    const userData = getUserData();
    if (!userData) {
      setCart([]);
      prevUserId.current = null;
      return;
    }
    // Aynı kullanıcı için tekrar yükleme yapma
    if (prevUserId.current === userData.id) return;
    prevUserId.current = userData.id;
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/user/cart/${userData.id}`);
      if (response.data.success) {
        const cartItems = response.data.cart.map(item => ({
          id: item.product_id,
          name: item.product_name,
          price: item.product_price,
          image_url: item.product_image_url,
          quantity: item.quantity,
          cart_item_id: item.id
        }));
        setCart(cartItems);
      }
    } catch (error) {
      console.error("Sepet yüklenemedi:", error);
      setCart([]);
    } finally {
      setLoading(false);
    }
  };

  // İlk yüklemede ve kullanıcı değiştiğinde sepeti yükle
  useEffect(() => {
    loadUserCart();
    // eslint-disable-next-line
  }, []);

  // Sadece userData değiştiğinde sepeti yükle
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === "userData" || e.key === "userLoggedIn") {
        prevUserId.current = null; // Kullanıcı değiştiyse tekrar yükle
        loadUserCart();
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const addToCart = async (product) => {
    const userData = getUserData();
    
    if (!userData) {
      setCart(prev => {
        const found = prev.find(item => item.id === product.id);
        if (found) {
          return prev.map(item =>
            item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
          );
        } else {
          return [...prev, { ...product, quantity: 1 }];
        }
      });
      return;
    }

    try {
      await axios.post(`http://localhost:8000/user/cart/${userData.id}/add`, {
        product_id: product.id,
        quantity: 1
      });
      prevUserId.current = null; // Zorunlu reload için
      await loadUserCart();
    } catch (error) {
      console.error("Ürün sepete eklenemedi:", error);
    }
  };

  const removeFromCart = async (productId) => {
    const userData = getUserData();
    
    if (!userData) {
      setCart(prev => prev.filter(item => item.id !== productId));
      return;
    }

    const cartItem = cart.find(item => item.id === productId);
    if (cartItem && cartItem.cart_item_id) {
      try {
        await axios.delete(`http://localhost:8000/user/cart/${userData.id}/remove/${cartItem.cart_item_id}`);
        prevUserId.current = null;
        await loadUserCart();
      } catch (error) {
        console.error("Ürün sepetten kaldırılamadı:", error);
      }
    }
  };

  const updateQuantity = async (productId, quantity) => {
    const userData = getUserData();
    
    if (!userData) {
      setCart(prev => {
        if (quantity <= 0) {
          return prev.filter(item => item.id !== productId);
        }
        return prev.map(item =>
          item.id === productId ? { ...item, quantity } : item
        );
      });
      return;
    }

    const cartItem = cart.find(item => item.id === productId);
    if (cartItem && cartItem.cart_item_id) {
      try {
        await axios.put(`http://localhost:8000/user/cart/${userData.id}/update/${cartItem.cart_item_id}?quantity=${quantity}`);
        prevUserId.current = null;
        await loadUserCart();
      } catch (error) {
        console.error("Sepet güncellenemedi:", error);
      }
    }
  };

  const clearCart = async () => {
    const userData = getUserData();
    
    if (!userData) {
      setCart([]);
      return;
    }

    try {
      await axios.delete(`http://localhost:8000/user/cart/${userData.id}/clear`);
      setCart([]);
      prevUserId.current = null;
    } catch (error) {
      console.error("Sepet temizlenemedi:", error);
    }
  };

  const getTotalPrice = () => {
    return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{ 
      cart, 
      addToCart, 
      removeFromCart, 
      updateQuantity,
      clearCart, 
      getTotalPrice,
      loading,
      loadUserCart
    }}>
      {children}
    </CartContext.Provider>
  );
} 