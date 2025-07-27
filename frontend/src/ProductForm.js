import React, { useState } from "react";
import axios from "axios";

const CATEGORY_OPTIONS = [
  { value: "anahtarlik", label: "Anahtarlık Şablonları" },
  { value: "yedek", label: "Araba Yedek Parçaları" },
  { value: "hediyelik", label: "Hediyelik & Dekorasyon Eşyaları" },
];

function ProductForm({ onProductAdded }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [stock, setStock] = useState("");
  const [category, setCategory] = useState(CATEGORY_OPTIONS[0].value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/products/", {
        name,
        description,
        price: parseFloat(price),
        image_url: imageUrl,
        stock: parseInt(stock),
        category
      });
      setName("");
      setDescription("");
      setPrice("");
      setImageUrl("");
      setStock("");
      setCategory(CATEGORY_OPTIONS[0].value);
      if (onProductAdded) onProductAdded();
    } catch (error) {
      alert("Ürün eklenirken hata oluştu!");
    }
  };

  return (
    <form className="product-form" onSubmit={handleSubmit}>
      <h2>Yeni Ürün Ekle</h2>
      <input
        type="text"
        placeholder="Ürün Adı"
        value={name}
        onChange={e => setName(e.target.value)}
        required
      />
      <select value={category} onChange={e => setCategory(e.target.value)} required>
        {CATEGORY_OPTIONS.map(opt => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
      <input
        type="number"
        placeholder="Fiyat (TL)"
        value={price}
        onChange={e => setPrice(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Stok"
        value={stock}
        onChange={e => setStock(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Görsel URL"
        value={imageUrl}
        onChange={e => setImageUrl(e.target.value)}
      />
      <textarea
        placeholder="Açıklama"
        value={description}
        onChange={e => setDescription(e.target.value)}
        required
      />
      <button type="submit">Ekle</button>
    </form>
  );
}

export default ProductForm; 