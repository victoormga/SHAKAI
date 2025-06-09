import React, { useState, useEffect } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(async () => {
      if (query.trim().length === 0) {
        setResults([]);
        return;
      }
      try {
        const res = await api.get(`/search/users/?search=${query}`);
        setResults(res.data);
      } catch (err) {
        console.error(err);
        setError("Error al buscar usuarios.");
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="max-w-lg mx-auto mt-6">
      <h2 className="text-2xl mb-4">Buscar Usuarios</h2>
      <input
        type="text"
        placeholder="Escribe el nombre de usuario..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full border px-2 py-1 rounded"
      />
      {error && <p className="text-red-500">{error}</p>}
      <div className="mt-4 space-y-2">
        {results.map((perfil) => (
          <div
            key={perfil.user}
            onClick={() => navigate(`/profiles/${perfil.user}`)}
            className="flex items-center space-x-2 cursor-pointer hover:bg-gray-100 p-2 rounded"
          >
            {perfil.profile_image ? (
              <img
                src={perfil.profile_image}
                alt="avatar"
                className="w-8 h-8 rounded-full object-cover"
              />
            ) : (
              <div className="w-8 h-8 bg-gray-300 rounded-full" />
            )}
            <div>
              <p className="font-medium">{perfil.display_name}</p>
              <p className="text-xs text-gray-500">
                {perfil.is_blocked ? "Bloqueado"
                  : perfil.is_private ? "Privado"
                  : "Público"
                }
              </p>
              {perfil.is_blocked && (
                <button
                  onClick={async () => {
                    await api.delete(`/blocks/unblock/${perfil.user}/`);
                    // refrescar búsqueda tras desbloquear
                    setResults((prev) =>
                      prev.map(p =>
                        p.user === perfil.user ? { ...p, is_blocked: false } : p
                      )
                    );
                  }}
                  className="ml-auto text-sm text-blue-600"
                >
                  Desbloquear
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Search;