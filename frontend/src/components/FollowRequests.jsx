// src/components/FollowRequests.jsx
import React, { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function FollowRequests() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const res = await api.get("/follows/requests/");
        // res.data = [{ follow_id, follower_id, follower_display_name }, ...]
        setRequests(res.data);
      } catch (err) {
        console.error("Error al cargar solicitudes:", err);
        setError("No se pudieron cargar solicitudes.");
      }
      setLoading(false);
    };
    fetchRequests();
  }, []);

  const acceptRequest = async (followId) => {
    try {
      await api.post(`/follows/accept/${followId}/`);
      // Quitamos la solicitud de la lista local
      setRequests((prev) => prev.filter((r) => r.follow_id !== followId));
    } catch (err) {
      console.error("Error al aceptar solicitud:", err);
      alert("No se pudo aceptar la solicitud.");
    }
  };

  if (loading) return <p className="p-4">Cargando solicitudes...</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;
  if (requests.length === 0)
    return <p className="p-4">No tienes solicitudes pendientes.</p>;

  return (
    <div className="space-y-4 p-4">
      <h2 className="text-xl font-semibold mb-4">Solicitudes de Seguimiento</h2>
      {requests.map((req) => (
        <div
          key={req.follow_id}
          className="p-3 flex justify-between items-center bg-white shadow rounded"
        >
          <span>{req.follower_display_name} quiere seguirte</span>
          <div className="space-x-2">
            <button
              onClick={() => acceptRequest(req.follow_id)}
              className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
            >
              Aceptar
            </button>
            <button
              onClick={() => {
                // Simple “rechazar” equivale a borrar la relación pendiente
                api.delete(`/unfollow/${req.follower_id}/`).then(() => {
                  setRequests((prev) =>
                    prev.filter((r) => r.follow_id !== req.follow_id)
                  );
                });
              }}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Rechazar
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
