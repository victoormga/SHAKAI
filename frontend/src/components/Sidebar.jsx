// src/components/Sidebar.jsx
import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { Home, User, Search, PlusSquare } from "lucide-react";
import { useAuth } from "../context/AuthContext";

function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user) return null;

  const links = [
    { name: "Inicio", path: "/", icon: <Home size={20} /> },
    { name: "Buscar", path: "/search", icon: <Search size={20} /> },
    { name: "Crear", path: "/create-post", icon: <PlusSquare size={20} /> },
    { name: "Mi Perfil", path: "/profile", icon: <User size={20} /> },
  ];

  return (
    <div className="w-20 h-screen border-r flex flex-col items-center py-4 space-y-6 bg-white">
      {links.map((link) => (
        <NavLink
          key={link.name}
          to={link.path}
          className={({ isActive }) =>
            `flex flex-col items-center ${
              isActive ? "text-blue-600" : "text-gray-600 hover:text-gray-800"
            }`
          }
        >
          {link.icon}
          <span className="text-xs mt-1">{link.name}</span>
        </NavLink>
      ))}
      <button
        onClick={() => logout()}
        className="mt-auto text-red-500 hover:text-red-700 text-sm"
      >
        Cerrar Sesión
      </button>
    </div>
  );
}

export default Sidebar;
