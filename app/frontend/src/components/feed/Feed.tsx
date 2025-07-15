import React from 'react';
import PostListAdvanced from '../posts/PostListAdvanced';

const Feed: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <PostListAdvanced 
        showUsername={true}
        initialFilters={{
          visibility: 'public',
          sort_by: 'created_at',
          sort_order: 'desc',
          per_page: 10
        }}
      />
    </div>
  );
};

export default Feed;