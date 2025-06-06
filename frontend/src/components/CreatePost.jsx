import React, { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function CreatePost() {
  const [caption, setCaption] = useState("");
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!file) {
      setError("Debes seleccionar un archivo.");
      return;
    }
    const fd = new FormData();
    fd.append("file", file);
    fd.append("caption", caption);
    try {
      await api.post("/posts/create/", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Error al crear la publicación.");
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-6 p-6 border rounded-lg">
      <h2 className="text-2xl mb-4">Crear Publicación</h2>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Imagen/Video:</label>
          <input type="file" onChange={handleFileChange} />
        </div>
        <div>
          <label>Texto (opcional):</label>
          <textarea
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            className="w-full border px-2 py-1 rounded"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-1 rounded"
        >
          Publicar
        </button>
      </form>
    </div>
  );
}

export default CreatePost;