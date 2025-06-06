import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

function EditProfile() {
  const { user, setUser } = useAuth();
  const [formData, setFormData] = useState({
    display_name: "",
    bio: "",
    is_private: false,
    profile_image: null,
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (user && user.profile) {
      setFormData({
        display_name: user.profile.display_name || "",
        bio: user.profile.bio || "",
        is_private: user.profile.is_private,
        profile_image: null,
      });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setFormData({ ...formData, [name]: checked });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, profile_image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const fd = new FormData();
    fd.append("display_name", formData.display_name);
    fd.append("bio", formData.bio);
    fd.append("is_private", formData.is_private);
    if (formData.profile_image) {
      fd.append("profile_image", formData.profile_image);
    }
    try {
      const res = await api.patch("/auth/me/profile/", fd);
      setUser((prev) => ({
        ...prev,
        profile: res.data,
      }));
      navigate("/profile");
    } catch (err) {
      console.error(err);
      setError("No se pudo actualizar el perfil.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-6 p-6 border rounded-lg">
      <h2 className="text-2xl mb-4">Editar Perfil</h2>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Nombre de Usuario:</label>
          <input
            type="text"
            name="display_name"
            value={formData.display_name}
            onChange={handleChange}
            required
            className="w-full border px-2 py-1 rounded"
          />
        </div>
        <div>
          <label>Bio:</label>
          <textarea
            name="bio"
            value={formData.bio}
            onChange={handleChange}
            className="w-full border px-2 py-1 rounded"
          />
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="is_private"
            checked={formData.is_private}
            onChange={handleChange}
          />
          <label>Cuenta Privada</label>
        </div>
        <div>
          <label>Imagen de Perfil:</label>
          <input type="file" onChange={handleFileChange} />
        </div>
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-1 rounded"
        >
          Guardar Cambios
        </button>
      </form>
    </div>
  );
}

export default EditProfile;