import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

import Login from "./components/Login";
import Register from "./components/Register";
import Feed from "./components/Feed";
import Profile from "./components/Profile";
import EditProfile from "./components/EditProfile";
import CreatePost from "./components/CreatePost";
import Search from "./components/Search";
import Sidebar from "./components/Sidebar";
import FollowRequests from "./components/FollowRequests";
import Notifications from "./components/Notifications";

function PrivateRoute({ children }) {
  const { user, loadingAuth } = useAuth();
  if (loadingAuth) return <p>Cargando...</p>;
  return user ? children : <Navigate to="/login" replace />;
}

function AppContent() {
  const location = useLocation();

  // Rutas donde NO queremos mostrar el sidebar
  const hiddenSidebarRoutes = ["/login", "/register", "/reset-password"];
  const shouldHideSidebar = hiddenSidebarRoutes.some((route) =>
    location.pathname.startsWith(route)
  );

  return (
    <div className="flex h-screen overflow-hidden">
      {!shouldHideSidebar && <Sidebar />}
      <div className={`${shouldHideSidebar ? "w-full" : "flex-1"} p-4 bg-gray-50 overflow-y-auto`}>
        <Routes>
          {/* Rutas protegidas */}
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Feed />
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          />
          <Route
            path="/profiles/:userId"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          />
          <Route
            path="/edit-profile"
            element={
              <PrivateRoute>
                <EditProfile />
              </PrivateRoute>
            }
          />
          <Route
            path="/create-post"
            element={
              <PrivateRoute>
                <CreatePost />
              </PrivateRoute>
            }
          />
          <Route
            path="/search"
            element={
              <PrivateRoute>
                <Search />
              </PrivateRoute>
            }
          />
          <Route
            path="/follow-requests"
            element={
              <PrivateRoute>
                <FollowRequests />
              </PrivateRoute>
            }
          />
          <Route
            path="/notifications"
            element={
              <PrivateRoute>
                <Notifications />
              </PrivateRoute>
            }
          />
          {/* Rutas públicas (sin sidebar) */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Cualquier otra ruta redirige a "/" */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}