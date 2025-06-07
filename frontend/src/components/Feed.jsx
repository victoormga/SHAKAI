import React, { useState, useEffect } from "react";
import api from "../services/api";
import PostCard from "./PostCard";

function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const res = await api.get("/posts/feed/");
        setPosts(res.data);
      } catch (err) {
        console.error(err);
        setError("No se pueden cargar las publicaciones.");
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);

  if (loading) return <p>Cargando publicaciones...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (posts.length === 0) return <p>No hay publicaciones disponibles.</p>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} refreshFeed={() => {
          // recargar posts
          setPosts((prev) => prev.filter((p) => p.id !== post.id) || []);
        }} />
      ))}
    </div>
  );
}

export default Feed;