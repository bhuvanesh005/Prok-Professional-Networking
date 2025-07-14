import React, { useEffect, useState } from 'react';
import { postsApi } from '../posts/api';
import type { Post } from '../../types';
import PostList from '../posts/PostList';

const Feed: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const fetchedPosts = await postsApi.getPosts();
        setPosts(fetchedPosts);
      } catch (err) {
        setError('Failed to fetch posts. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <PostList posts={posts} />
    </div>
  );
};

export default Feed;