import React, { useEffect, useState } from 'react';
import { Bell, Check } from 'lucide-react';
import api from '../services/api';

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchNotifs = async () => {
      try {
        const res = await api.get('/notifications/');
        setNotifications(res.data);
      } catch (err) {
        console.error(err);
        setError('No se pudieron cargar las notificaciones.');
      }
      setLoading(false);
    };
    fetchNotifs();
  }, []);

  const markRead = async (id) => {
    try {
      await api.post(`/notifications/${id}/read/`);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch (err) {
      console.error(err);
      alert('No se pudo marcar como leída.');
    }
  };

  if (loading) return <p className="p-4">Cargando notificaciones...</p>;
  if (error) return <p className="p-4 text-red-600">{error}</p>;
  if (notifications.length === 0)
    return <p className="p-4">No tienes notificaciones.</p>;

  return (
    <div className="space-y-4 p-4 max-w-lg mx-auto">
      <h2 className="text-xl font-semibold mb-4 flex items-center">
        <Bell className="mr-2" /> Notificaciones
      </h2>
      {notifications.map((n) => (
        <div
          key={n.id}
          className={`p-3 flex justify-between items-center border rounded ${
            n.is_read ? 'bg-gray-50' : 'bg-white'
          }`}
        >
          <div className="flex-1">
            <p className="text-sm">
              {n.notif_type === 'like' && (
                <><strong>{n.sender_display_name}</strong> te dio like en su publicación.</>
              )}
              {n.notif_type === 'comment' && (
                <><strong>{n.sender_display_name}</strong> comentó tu publicación.</>
              )}
              {n.notif_type === 'follow_request' && (
                <><strong>{n.sender_display_name}</strong> solicitó seguirte.</>
              )}
              {n.notif_type === 'follow_accepted' && (
                <><strong>{n.sender_display_name}</strong> aceptó tu solicitud.</>
              )}
            </p>
            <p className="text-xs text-gray-400 mt-1">{new Date(n.created_at).toLocaleString()}</p>
          </div>
          {!n.is_read && (
            <button
              onClick={() => markRead(n.id)}
              className="ml-4 p-1 rounded-full hover:bg-gray-200 focus:outline-none"
              title="Marcar como leído"
            >
              <Check size={16} />
            </button>
          )}
        </div>
      ))}
    </div>
  );
}