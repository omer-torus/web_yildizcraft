import React, { useState } from "react";
import axios from "axios";

function CustomDesignForm() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

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

      // Sonra custom design kaydını oluştur
      const customDesignData = {
        customer_name: name,
        customer_phone: phone,
        description: description,
        file_path: uploadResponse.data.filename,
        created_at: new Date().toISOString()
      };

      await axios.post("http://localhost:8000/custom-designs/", customDesignData);
      
      setMessage("Tasarım talebiniz başarıyla gönderildi! En kısa sürede size dönüş yapacağız.");
      setName("");
      setPhone("");
      setDescription("");
      setFile(null);
    } catch (error) {
      setMessage("Gönderim sırasında hata oluştu! Lütfen tekrar deneyin.");
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
    </form>
  );
}

export default CustomDesignForm; 