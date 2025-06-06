import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

function PostModal({ post, onClose, refreshFeed }) {
  const { user } = useAuth();
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [hasLiked, setHasLiked] = useState(false);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  // Cargar estado de “hasLiked” y comentarios
  useEffect(() => {
    const fetchData = async () => {
      try {
        const likeRes = await api.get(`/likes/has-liked/${post.id}/`);
        setHasLiked(likeRes.data.has_liked);
        const commentsRes = await api.get(`/comments/post/${post.id}/comments/`);
        setComments(commentsRes.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, [post.id]);

  const handleLike = async () => {
    try {
      const res = await api.post(`/likes/toggle/${post.id}/`);
      if (res.data.liked) {
        setLikesCount((prev) => prev + 1);
        setHasLiked(true);
      } else {
        setLikesCount((prev) => prev - 1);
        setHasLiked(false);
      }
    } catch (err) {
      console.error(err);
      alert("No se pudo actualizar el like.");
    }
  };

  const handleDeletePost = async () => {
    if (!window.confirm("¿Seguro que deseas eliminar esta publicación?")) return;
    try {
      await api.delete(`/posts/${post.id}/delete/`);
      refreshFeed();
      onClose();
    } catch (err) {
      console.error(err);
      alert("No se pudo eliminar la publicación.");
    }
  };

  const handleAddComment = async () => {
    if (!newComment.trim()) return;
    try {
      const res = await api.post(`/comments/post/${post.id}/comments/`, {
        content: newComment,
      });
      setComments((prev) => [...prev, res.data]);
      setNewComment("");
    } catch (err) {
      console.error(err);
      alert("Error al comentar.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg w-3/4 max-w-3xl p-4 space-y-4 relative">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-600 hover:text-black"
        >
          ✕
        </button>
        <div className="flex flex-col md:flex-row">
          <div className="md:w-1/2 flex items-center justify-center border-r">
            {post.file_url ? (
              <img src={post.file_url} alt="Post" className="max-h-96 object-contain" />
            ) : null}
          </div>
          <div className="md:w-1/2 p-4 space-y-4">
            <div className="flex justify-between items-center">
              <p className="font-semibold">{post.user_display_name}</p>
              {user.id === post.user && (
                <button
                  onClick={handleDeletePost}
                  className="text-red-500 hover:text-red-700"
                >
                  Eliminar
                </button>
              )}
            </div>
            <p className="text-gray-800">{post.caption}</p>
            <div className="flex items-center space-x-2">
              <button onClick={handleLike} className="flex items-center space-x-1">
                {hasLiked ? "💖" : "🤍"} <span>{likesCount}</span>
              </button>
            </div>
            <hr />
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {comments.map((c) => (
                <div key={c.id} className="border-b pb-2">
                  <p className="text-sm font-medium">
                    {c.user_display_name}:
                  </p>
                  <p className="text-sm">{c.content}</p>
                </div>
              ))}
            </div>
            <div className="flex space-x-2 items-center">
              <input
                type="text"
                placeholder="Agrega un comentario..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                className="flex-1 border px-2 py-1 rounded"
              />
              <button
                onClick={handleAddComment}
                className="bg-blue-600 text-white px-3 py-1 rounded"
              >
                Comentar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PostModal;