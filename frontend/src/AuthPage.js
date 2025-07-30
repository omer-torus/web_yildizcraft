import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./AuthPage.css";

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    full_name: "",
    phone: "",
    address: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (isLogin) {
        // Admin kontrolü
        if (formData.username === "admin") {
          const response = await axios.post("http://localhost:8000/admin/login", {
            username: formData.username,
            password: formData.password
          });

          if (response.data.success) {
            localStorage.setItem("adminLoggedIn", "true");
            localStorage.setItem("adminUser", JSON.stringify(response.data.admin));
            navigate("/admin");
            return;
          }
        } else {
          // Normal kullanıcı girişi
          const response = await axios.post("http://localhost:8000/user/login", {
            username: formData.username,
            password: formData.password
          });

          if (response.data.success) {
            localStorage.setItem("userLoggedIn", "true");
            localStorage.setItem("userData", JSON.stringify(response.data.user));
            
            // Storage event'ini tetikle
            window.dispatchEvent(new Event('storage'));
            
            navigate("/");
            return;
          }
        }
      } else {
        // Kullanıcı kaydı
        const response = await axios.post("http://localhost:8000/user/register", formData);

        if (response.data.success) {
          setError("Kayıt başarılı! Şimdi giriş yapabilirsiniz.");
          setIsLogin(true);
          setFormData({
            username: formData.username,
            password: formData.password,
            email: "",
            full_name: "",
            phone: "",
            address: ""
          });
          return;
        }
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.detail) {
        setError(error.response.data.detail);
      } else {
        setError("Bir hata oluştu. Lütfen tekrar deneyin.");
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setError("");
    setFormData({
      username: "",
      password: "",
      email: "",
      full_name: "",
      phone: "",
      address: ""
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-header">
          <h1>{isLogin ? "Giriş Yap" : "Üye Ol"}</h1>
          <p>YildizCraft3D Hesabınız</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Kullanıcı Adı</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Şifre</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={loading}
            />
          </div>

          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="email">E-posta</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="full_name">Ad Soyad</label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleInputChange}
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Telefon</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="address">Adres</label>
                <textarea
                  id="address"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  required
                  disabled={loading}
                  rows="3"
                />
              </div>
            </>
          )}
          
          {error && <div className="error-message">{error}</div>}
          
          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? (isLogin ? "Giriş Yapılıyor..." : "Kayıt Oluşturuluyor...") : (isLogin ? "Giriş Yap" : "Üye Ol")}
          </button>
        </form>

        <div className="auth-toggle">
          <button onClick={toggleMode} className="toggle-button">
            {isLogin ? "Hesabınız yok mu? Üye olun" : "Zaten hesabınız var mı? Giriş yapın"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default AuthPage; 