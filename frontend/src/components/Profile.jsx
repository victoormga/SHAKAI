import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import PostCard from "./PostCard";

function Profile() {
  const { user, setUser } = useAuth();
  const navigate = useNavigate();
  const { userId } = useParams(); // si es undefined, es mi perfil
  const isOwnProfile = !userId || parseInt(userId) === user.id;

  const [profileData, setProfileData] = useState(null);
  const [posts, setPosts] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [error, setError] = useState("");

  // Cargar datos del perfil (propio o ajeno)
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        if (isOwnProfile) {
          const res = await api.get("/auth/me/profile/");
          setProfileData(res.data);
          // Cargar mis posts
          const postsRes = await api.get(`/posts/user/${user.id}/`);
          setPosts(postsRes.data);
        } else {
          const res = await api.get(`auth/profiles/${userId}/`);
          setProfileData(res.data);
          // Cargar posts de ese usuario
          const postsRes = await api.get(`/posts/user/${userId}/`);
          setPosts(postsRes.data);
          // Comprobar si sigo a ese usuario
          const followRes = await api.get(`/follows/status/${userId}/`);
          setIsFollowing(followRes.data.is_following);
        }
      } catch (err) {
        console.error(err);
        setError("No se pudieron cargar los datos del perfil.");
      }
    };
    fetchProfile();
  }, [userId, isOwnProfile, user.id]);

  const handleFollow = async () => {
    try {
      await api.post(`/follows/${userId}/`);
      setIsFollowing(true);
    } catch (err) {
      console.error(err);
      alert("No se pudo enviar la solicitud de seguimiento.");
    }
  };

  const handleUnfollow = async () => {
    try {
      await api.delete(`/follows/unfollow/${userId}/`);
      setIsFollowing(false);
    } catch (err) {
      console.error(err);
      alert("No se pudo dejar de seguir.");
    }
  };

  const handleBlock = async () => {
    if (!window.confirm("¿Bloquear a este usuario?")) return;
    try {
      await api.post(`/blocks/${userId}/`);
      navigate("/");
    } catch (err) {
      console.error(err);
      alert("No se pudo bloquear.");
    }
  };

  const handleUnblock = async () => {
    try {
      await api.delete(`/blocks/unblock/${userId}/`);
      alert("Usuario desbloqueado.");
    } catch (err) {
      console.error(err);
      alert("No se pudo desbloquear.");
    }
  };

  if (!profileData) return <p>Cargando perfil...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <div className="flex items-center space-x-4">
        {profileData.profile_image ? (
          <img
            src={profileData.profile_image}
            alt="Avatar"
            className="w-24 h-24 rounded-full object-cover"
          />
        ) : (
          <div className="w-16 h-16 bg-gray-300 rounded-full" />
        )}
        <div>
          <h2 className="text-2xl font-semibold">{profileData.display_name}</h2>
          <p className="text-gray-600">{profileData.email}</p>
          <p className="text-gray-500">{profileData.bio}</p>
          <p className="text-sm text-gray-400">
            {profileData.is_private ? "Cuenta Privada" : "Cuenta Pública"}
          </p>
          {/* Contadores de publicaciones, seguidores y siguiendo */}
          <div className="mt-2 flex space-x-4 text-sm text-gray-700">
            <span><strong>{profileData.posts_count}</strong> publicaciones</span>
            <span><strong>{profileData.followers_count}</strong> seguidores</span>
            <span><strong>{profileData.following_count}</strong> siguiendo</span>
          </div>
        </div>
      </div>

      {isOwnProfile ? (
        <button
          onClick={() => navigate("/edit-profile")}
          className="bg-blue-600 text-white px-4 py-1 rounded"
        >
          Editar Perfil
        </button>
      ) : (
        <div className="flex space-x-2">
          {isFollowing ? (
            <button
              onClick={handleUnfollow}
              className="bg-red-600 text-white px-4 py-1 rounded"
            >
              Dejar de seguir
            </button>
          ) : (
            <button
              onClick={handleFollow}
              className="bg-green-600 text-white px-4 py-1 rounded"
            >
              {profileData.is_private ? "Solicitar seguir" : "Seguir"}
            </button>
          )}
          <button
            onClick={handleBlock}
            className="bg-gray-800 text-white px-4 py-1 rounded"
          >
            Bloquear
          </button>
          <button
            onClick={handleUnblock}
            className="bg-yellow-600 text-white px-4 py-1 rounded"
          >
            Desbloquear
          </button>
        </div>
      )}

      <hr />

      <div>
        <h3 className="text-xl mb-2">Publicaciones</h3>
        {posts.length === 0 ? (
          <p>No tiene publicaciones.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                refreshFeed={() => {
                  // Quitar post de la vista si lo borró el autor
                  setPosts((prev) => prev.filter((p) => p.id !== post.id));
                }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
