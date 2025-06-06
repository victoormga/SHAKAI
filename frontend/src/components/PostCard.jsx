import React, { useState } from "react";
import PostModal from "./PostModal";

function PostCard({ post, refreshFeed }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <div
        className="border rounded overflow-hidden cursor-pointer"
        onClick={() => setOpen(true)}
      >
        {post.file_url ? (
          <img
            src={post.file_url}
            alt="Post"
            className="object-cover w-full h-64"
          />
        ) : null}
        <div className="p-2">
          <p className="text-sm text-gray-700">{post.caption}</p>
          <p className="text-xs text-gray-500">{post.user_display_name}</p>
        </div>
      </div>
      {open && (
        <PostModal
          post={post}
          onClose={() => setOpen(false)}
          refreshFeed={refreshFeed}
        />
      )}
    </>
  );
}

export default PostCard;