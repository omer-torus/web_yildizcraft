import React, { useState } from "react";
import axios from "axios";

function CustomDesignForm() {
  const [name, setName] = useState("");
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
    const formData = new FormData();
    formData.append("name", name);
    formData.append("description", description);
    formData.append("file", file);
    try {
      await axios.post("http://localhost:8000/upload-stl/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setMessage("Dosyanız başarıyla yüklendi!");
      setName("");
      setDescription("");
      setFile(null);
    } catch (error) {
      setMessage("Yükleme sırasında hata oluştu!");
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
      {message && <p>{message}</p>}
    </form>
  );
}

export default CustomDesignForm; 