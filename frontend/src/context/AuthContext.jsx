import React, { createContext, useContext, useState, useEffect } from "react";
import api from "../services/api";

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loadingAuth, setLoadingAuth] = useState(true);

  // Al montar, verifico si hay token y cargo mi perfil
  useEffect(() => {
    const initializeAuth = async () => {
      const access = localStorage.getItem("access_token");
      if (access) {
        try {
          const res = await api.get("/auth/me/");
          setUser(res.data);
        } catch (err) {
          console.error("Error al cargar usuario:", err);
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
      }
      setLoadingAuth(false);
    };
    initializeAuth();
  }, []);

  // Función de login
  const login = async (email, password) => {
    const data = await api.post("/auth/login/", { email, password });
    localStorage.setItem("access_token", data.data.access);
    localStorage.setItem("refresh_token", data.data.refresh);
    api.defaults.headers.common["Authorization"] = `Bearer ${data.data.access}`;

    // Obtener mi perfil
    const meRes = await api.get("/auth/me/");
    setUser(meRes.data);
  };

  // Función de logout
  const logout = () => {
    const r = localStorage.getItem("refresh_token");
    if (r) api.post("/auth/logout/", { refresh: r }).catch(console.error);
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    window.location.href = "/login";
  };

  const value = {
    user,
    setUser,
    login,
    logout,
    loadingAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}