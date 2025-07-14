import React from 'react';
import type { Post } from '../../types';

interface PostListProps {
  posts: Post[];
  showUsername?: boolean;
}

const PostList: React.FC<PostListProps> = ({ posts, showUsername = true }) => {
  return (
    <div className="space-y-6">
      {posts.map((post) => (
        <div key={post.id} className="bg-white shadow-md rounded-lg p-4">
          {showUsername && (
            <div className="flex items-center mb-2">
              <div className="font-bold">{post.user}</div>
            </div>
          )}
          <h3 className="text-xl font-bold mb-2">{post.title}</h3>
          <div
            className="prose max-w-none"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />
          {post.media_url && (
            <div className="mt-4">
              {post.media_url.endsWith('.mp4') || post.media_url.endsWith('.mov') ? (
                <video src={`http://localhost:5000${post.media_url}`} controls className="max-w-full h-auto" />
              ) : (
                <img src={`http://localhost:5000${post.media_url}`} alt="Post media" className="max-w-full h-auto" />
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default PostList;