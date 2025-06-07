// src/components/Sidebar.jsx
import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import {
  Home,
  Search,
  Mail,
  Heart,
  PlusSquare,
  User,
  MoreHorizontal,
  LogOut,
} from "lucide-react";

// Lista de ítems del menú. Cada objeto puede tener:
// - icon: el componente SVG (Lucide React)
// - label: texto a mostrar cuando el sidebar esté expandido
// - route: si existe, al hacer click navegamos a esa ruta
const menuItems = [
  { icon: <Home size={24} />, label: "Inicio", route: "/feed" },
  { icon: <Search size={24} />, label: "Búsqueda", route: "/search" },
  { icon: <Heart size={24} />, label: "Notificaciones", route: "/notifications" },
  { icon: <Mail size={24} />, label: "Solicitudes", route: "/follow-requests" },
  { icon: <PlusSquare size={24} />, label: "Crear", route: "/create-post" },
  { icon: <User size={24} />, label: "Perfil", route: "/profile" },
  { icon: <MoreHorizontal size={24} />, label: "Más" },
];

export default function Sidebar() {
  const [expanded, setExpanded] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    // El contenedor sticky / fixed del sidebar
    <div
      // Al pasar el ratón, expandimos; al salir, contraemos
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => setExpanded(false)}
      className={`
        ${expanded ? "w-64" : "w-20"}   /* ancho: 64 si está expandido, 20 si contraído */
        bg-white
        h-full              /* ocupa todo el alto del contenedor flex (h-screen desde App) */
        border-r border-gray-200
        flex flex-col justify-between
        transition-all duration-200 ease-in-out
        z-50
      `}
    >
      {/* Bloque superior: Logo */}
      <div
        className={`
          mb-4
          px-3
          flex items-center
          h-16
          ${expanded ? "justify-start " : "justify-center"}
        `}
      >
        {expanded ? (
          // Si está expandido mostramos un logo amplio
          <img src="/nombre.png" alt="logo" className="w-32 h-7 " />
        ) : (
          // Si está contraído, mostramos solo el icono
          <img src="/logo.png" alt="logo" className="w-7 h-7 " />
        )}
      </div>

      {/* Menú principal */}
      <div className="flex-1 space-y-4">
        {menuItems.map((item, idx) => (
          <div
            key={idx}
            onClick={() => {
              if (item.route) {
                navigate(item.route);
              }
            }}
            className="
              flex items-center
              space-x-3
              px-6
              hover:bg-gray-100
              rounded-lg
              p-3
              cursor-pointer
              transition
            "
          >
            {item.icon}
            {expanded && <span className="text-gray-800">{item.label}</span>}
          </div>
        ))}
      </div>

      {/* Bloque inferior: Logout */}
      <div className="mb-4 px-2">
        <button
          onClick={handleLogout}
          className="
            flex items-center
            space-x-3
            hover:bg-red-100
            rounded-lg
            p-2
            w-full
            text-red-500
            transition
          "
        >
          <LogOut size={24} />
          {expanded && <span>Cerrar sesión</span>}
        </button>
      </div>
    </div>
  );
}
