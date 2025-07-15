import React, { useState, useEffect } from 'react';
import PostListAdvanced from './PostListAdvanced';

const PostListTest: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Simulate authentication for testing
  useEffect(() => {
    // Set a test token for API calls
    localStorage.setItem('token', 'test-token');
    setIsAuthenticated(true);
  }, []);

  if (!isAuthenticated) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b border-gray-200 p-4">
        <h1 className="text-2xl font-bold text-gray-900">Posts Test Page</h1>
        <p className="text-gray-600">Testing the posts listing functionality</p>
      </div>
      <PostListAdvanced />
    </div>
  );
};

export default PostListTest; 