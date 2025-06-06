import { X, Heart, MessageCircle, Trash2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function PostModal({ post, onClose, onDelete }) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [hasLiked, setHasLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likes_count || 0);

  // Verifica si es un video
  const isVideo = post.file.toLowerCase().endsWith(".mp4");

  // Carga comentarios y estado de like cuando se abre el modal
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Traer comentarios
        const commentsRes = await api.get(`/comments/post/${post.id}/comments/`);
        setComments(commentsRes.data);

        // Verificar si el usuario ya le dio like
        const likeRes = await api.get(`/likes/has-liked/${post.id}/`);
        setHasLiked(likeRes.data.has_liked);
      } catch (err) {
        console.error("Error al cargar datos del post:", err);
      }
    };
    fetchData();
  }, [post.id]);

  // Dar o quitar like
  const handleLike = async () => {
    try {
      const res = await api.post(`/likes/toggle/${post.id}/`);
      if (res.data.liked) {
        setHasLiked(true);
        setLikesCount((prev) => prev + 1);
      } else {
        setHasLiked(false);
        setLikesCount((prev) => Math.max(prev - 1, 0));
      }
    } catch (err) {
      console.error("Error al dar like:", err.response?.data || err);
      alert("No se pudo actualizar el like.");
    }
  };

  // Borrar post
  const handleDelete = async () => {
    const confirmDelete = window.confirm(
      "¿Estás seguro de que quieres borrar esta publicación?"
    );
    if (!confirmDelete) return;

    try {
      await api.delete(`/posts/${post.id}/delete/`);
      if (onDelete) onDelete(post.id);
      onClose();
    } catch (err) {
      console.error("Error al eliminar el post:", err);
      alert("No se pudo eliminar la publicación.");
    }
  };

  // Enviar nuevo comentario
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      const res = await api.post(`/comments/post/${post.id}/comments/`, {
        content: newComment.trim(),
      });
      setComments((prev) => [...prev, res.data]); // Añadir el nuevo comentario
      setNewComment(""); // Limpiar input
    } catch (err) {
      console.error("Error al publicar comentario:", err);
      alert("Error al publicar comentario.");
    }
  };

  return (
    // Overlay semitransparente + desenfoque
    <div className="fixed inset-0 bg-black bg-opacity-30 backdrop-blur-sm flex items-center justify-center z-50">
      {/* Modal contenedor: más grande (90vh) */}
      <div className="bg-white rounded-lg shadow-lg max-w-6xl w-full h-[90vh] flex relative overflow-hidden">
        {/* Botón de cerrar */}
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-gray-600 hover:text-gray-900 z-10"
          aria-label="Cerrar"
        >
          <X size={24} />
        </button>

        {/* Lado izquierdo: imagen o video */}
        <div className="w-1/2 h-full bg-black flex items-center justify-center">
          {isVideo ? (
            <video
              controls
              className="max-h-full max-w-full object-contain"
              src={post.file.startsWith("http") ? post.file : `http://localhost:8000${post.file}`}
            />
          ) : (
            <img
              src={post.file.startsWith("http") ? post.file : `http://localhost:8000${post.file}`}
              alt="post"
              className="max-h-full max-w-full object-contain"
            />
          )}
        </div>

        {/* Lado derecho: texto, likes, comentarios */}
        <div className="w-1/2 h-full flex flex-col justify-between p-6 overflow-y-auto">
          {/* Sección superior: caption + lista de comentarios */}
          <div className="flex-1">
            {/* Caption / Descripción */}
            <h2 className="font-bold text-lg mb-4">{post.caption}</h2>

            <div className="pt-4 border-t mt-4 space-y-2 text-sm">
              {comments.length === 0 ? (
                <p className="text-gray-500">Sin comentarios aún</p>
              ) : (
                comments.map((comment) => (
                  <div key={comment.id} className="pb-2 border-b">
                    <p className="text-sm font-medium">{comment.user_display_name}</p>
                    <p className="text-sm text-gray-700">{comment.content}</p>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Sección inferior: like, comentar, borrar */}
          <div className="pt-4 border-t mt-4">
            <div className="flex items-center gap-6 mb-4">
              {/* Like */}
              <button
                onClick={handleLike}
                className="flex items-center space-x-1 hover:text-red-500 focus:outline-none"
                title={hasLiked ? "Quitar like" : "Dar like"}
              >
                <Heart
                  size={24}
                  className={hasLiked ? "text-red-500" : "text-gray-600"}
                />
                <span className="text-gray-700">{likesCount}</span>
              </button>

              {/* Icono de comentarios (solo visual) */}
              <button
                onClick={() => {
                  // Para hacer foco en el input de comentario si se desea
                  document.getElementById("post-modal-input")?.focus();
                }}
                className="hover:text-gray-800 focus:outline-none"
                title="Comentar"
              >
                <MessageCircle size={24} className="text-gray-600" />
              </button>

              {/* Botón de eliminar, solo si es tu propio post */}
              {user?.id === post.user && (
                <button
                  onClick={handleDelete}
                  className="hover:text-red-700 focus:outline-none"
                  title="Eliminar publicación"
                >
                  <Trash2 size={24} className="text-red-500" />
                </button>
              )}
            </div>

            {/* Formulario para agregar comentario */}
            <form className="flex gap-2" onSubmit={handleSubmit}>
              <input
                id="post-modal-input"
                type="text"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Añade un comentario..."
                className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                type="submit"
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition text-sm"
              >
                Publicar
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}