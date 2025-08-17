import React, { useState } from "react";
import axios from "axios";
import "./CustomDesignForm.css";

function CustomDesignForm() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.name.toLowerCase().endsWith(".stl")) {
      setFile(selected);
    } else {
      setFile(null);
      alert("Sadece .stl dosyası yükleyebilirsiniz!");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Lütfen bir .stl dosyası seçin.");
      return;
    }

    try {
      // Önce dosyayı yükle
      const formData = new FormData();
      formData.append("name", name);
      formData.append("description", description);
      formData.append("file", file);
      
      const uploadResponse = await axios.post("http://localhost:8000/upload-stl/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      // Analiz sonuçlarını kaydet
      if (uploadResponse.data.analysis) {
        setAnalysis(uploadResponse.data.analysis);
      }

      // Sonra custom design kaydını oluştur
      const customDesignData = {
        customer_name: name,
        customer_phone: phone,
        description: description,
        file_path: uploadResponse.data.filename,
        created_at: new Date().toISOString()
      };

      console.log("Gönderilecek veri:", customDesignData);
      
      const customDesignResponse = await axios.post("http://localhost:8000/custom-designs/", customDesignData);
      console.log("Custom design response:", customDesignResponse.data);
      
      setMessage("Tasarım talebiniz başarıyla gönderildi! En kısa sürede size dönüş yapacağız.");
      setName("");
      setPhone("");
      setDescription("");
      setFile(null);
      setAnalysis(null);
    } catch (error) {
      console.error("Gönderim hatası:", error);
      if (error.response && error.response.data && error.response.data.detail) {
        setMessage(`Hata: ${error.response.data.detail}`);
      } else if (error.message) {
        setMessage(`Hata: ${error.message}`);
      } else {
        setMessage("Gönderim sırasında hata oluştu! Lütfen tekrar deneyin.");
      }
    }
  };

  return (
    <form className="custom-design-form" onSubmit={handleSubmit}>
      <h2>Kendi Tasarımını Gönder</h2>
      <input
        type="text"
        placeholder="Ad Soyad"
        value={name}
        onChange={e => setName(e.target.value)}
        required
      />
      <input
        type="tel"
        placeholder="Telefon Numarası"
        value={phone}
        onChange={e => setPhone(e.target.value)}
        required
      />
      <textarea
        placeholder="Açıklama"
        value={description}
        onChange={e => setDescription(e.target.value)}
        required
      />
      <input
        type="file"
        accept=".stl"
        onChange={handleFileChange}
        required
      />
      <button type="submit">Gönder</button>
      {message && <p className="form-message">{message}</p>}
      
      {/* Analiz sonuçları */}
      {analysis && (
        <div className="analysis-results">
          <h3>📊 STL Dosya Analizi</h3>
          <div className="analysis-grid">
            <div className="analysis-item">
              <span className="analysis-label">Filament Ağırlığı:</span>
              <span className="analysis-value">{analysis.weight_grams?.toFixed(1)} g</span>
            </div>
            <div className="analysis-item">
              <span className="analysis-label">Tahmini Baskı Süresi:</span>
              <span className="analysis-value">{analysis.print_time_hours?.toFixed(1)} saat</span>
            </div>
            <div className="analysis-item">
              <span className="analysis-label">Tahmini Satış Fiyatı:</span>
              <span className="analysis-value">{analysis.sales_price} TL</span>
            </div>
          </div>
          <p className="analysis-note">
            * Bu değerler tahminidir. Gerçek değerler baskı ayarlarına göre değişebilir.
          </p>
        </div>
      )}
    </form>
  );
}

export default CustomDesignForm; 