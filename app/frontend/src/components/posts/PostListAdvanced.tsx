import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { postsApi } from './api';
import { useDebounce } from '../../hooks/useDebounce';
import { useInfiniteScroll } from '../../hooks/useInfiniteScroll';
import LazyImage from '../common/LazyImage';
import type { Post, PostFilters, PopularTag } from '../../types';

interface PostListAdvancedProps {
  showUsername?: boolean;
  initialFilters?: PostFilters;
}

const PostListAdvanced: React.FC<PostListAdvancedProps> = ({ 
  showUsername = true, 
  initialFilters = {} 
}) => {
  // State management
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [categories, setCategories] = useState<string[]>([]);
  const [popularTags, setPopularTags] = useState<PopularTag[]>([]);
  
  // Filter states
  const [filters, setFilters] = useState<PostFilters>({
    page: 1,
    per_page: 10,
    sort_by: 'created_at',
    sort_order: 'desc',
    ...initialFilters,
  });
  
  const [searchInput, setSearchInput] = useState(filters.search || '');
  const [selectedCategory, setSelectedCategory] = useState(filters.category || '');
  const [selectedVisibility, setSelectedVisibility] = useState(filters.visibility || 'public');
  const [selectedTags, setSelectedTags] = useState(filters.tags || '');
  const [sortBy, setSortBy] = useState(filters.sort_by || 'created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>(filters.sort_order || 'desc');

  // Debounced search
  const debouncedSearch = useDebounce(searchInput, 500);
  const debouncedTags = useDebounce(selectedTags, 500);

  // Memoized current filters
  const currentFilters = useMemo(() => ({
    ...filters,
    search: debouncedSearch,
    category: selectedCategory,
    visibility: selectedVisibility,
    tags: debouncedTags,
    sort_by: sortBy,
    sort_order: sortOrder,
  }), [debouncedSearch, selectedCategory, selectedVisibility, debouncedTags, sortBy, sortOrder, filters]);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [categoriesRes, tagsRes] = await Promise.all([
          postsApi.getCategories(),
          postsApi.getPopularTags(20),
        ]);
        setCategories(categoriesRes.categories);
        setPopularTags(tagsRes.tags);
      } catch (err) {
        console.error('Failed to load initial data:', err);
      }
    };
    loadInitialData();
  }, []);

  // Fetch posts function
  const fetchPosts = useCallback(async (resetPosts = false) => {
    try {
      setLoading(true);
      setError(null);
      
      const filtersToUse = resetPosts 
        ? { ...currentFilters, page: 1 }
        : currentFilters;
      
      const response = await postsApi.getPosts(filtersToUse);
      
      if (resetPosts) {
        setPosts(response.posts);
      } else {
        setPosts(prev => [...prev, ...response.posts]);
      }
      
      setHasMore(response.pagination.has_next);
      setFilters(prev => ({ ...prev, page: response.pagination.page }));
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch posts');
    } finally {
      setLoading(false);
    }
  }, [currentFilters]);

  // Load more posts for infinite scroll
  const loadMorePosts = useCallback(async () => {
    if (!hasMore || loading) return;
    
    const nextPage = (filters.page || 1) + 1;
    setFilters(prev => ({ ...prev, page: nextPage }));
    
    try {
      const response = await postsApi.getPosts({ ...currentFilters, page: nextPage });
      setPosts(prev => [...prev, ...response.posts]);
      setHasMore(response.pagination.has_next);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load more posts');
    }
  }, [currentFilters, filters.page, hasMore, loading]);

  // Infinite scroll hook
  const { isFetching, lastElementRef } = useInfiniteScroll(loadMorePosts, hasMore);

  // Reset and fetch when filters change
  useEffect(() => {
    fetchPosts(true);
  }, [debouncedSearch, selectedCategory, selectedVisibility, debouncedTags, sortBy, sortOrder]);

  // Handle tag click
  const handleTagClick = (tag: string) => {
    const currentTags = selectedTags.split(',').filter(t => t.trim());
    if (currentTags.includes(tag)) {
      setSelectedTags(currentTags.filter(t => t !== tag).join(','));
    } else {
      setSelectedTags([...currentTags, tag].join(','));
    }
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchInput('');
    setSelectedCategory('');
    setSelectedVisibility('public');
    setSelectedTags('');
    setSortBy('created_at');
    setSortOrder('desc');
  };

  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
    });
  };

  // Get user initials for avatar
  const getUserInitials = (username: string) => {
    return username ? username.charAt(0).toUpperCase() : 'U';
  };

  // Handle like post
  const handleLike = async (postId: number) => {
    try {
      await postsApi.likePost(postId);
      // Update the post in the list
      setPosts(prev => prev.map(post => 
        post.id === postId 
          ? { ...post, likes_count: (post.likes_count || 0) + 1 }
          : post
      ));
    } catch (err) {
      console.error('Failed to like post:', err);
    }
  };

  // Handle share post
  const handleShare = (post: Post) => {
    if (navigator.share) {
      navigator.share({
        title: post.title,
        text: post.content.replace(/<[^>]*>/g, ''), // Remove HTML tags
        url: window.location.href,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(`${post.title}\n\n${post.content.replace(/<[^>]*>/g, '')}`);
      alert('Post link copied to clipboard!');
    }
  };

  // Render loading skeleton
  const renderSkeleton = () => (
    <div className="space-y-6">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
          <div className="flex items-center mb-4">
            <div className="w-10 h-10 bg-gray-300 rounded-full mr-3"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-300 rounded w-32 mb-1"></div>
              <div className="h-3 bg-gray-300 rounded w-24"></div>
            </div>
          </div>
          <div className="h-6 bg-gray-300 rounded w-3/4 mb-3"></div>
          <div className="space-y-2 mb-4">
            <div className="h-4 bg-gray-300 rounded"></div>
            <div className="h-4 bg-gray-300 rounded w-5/6"></div>
          </div>
          <div className="flex space-x-6">
            <div className="h-4 bg-gray-300 rounded w-16"></div>
            <div className="h-4 bg-gray-300 rounded w-20"></div>
            <div className="h-4 bg-gray-300 rounded w-16"></div>
          </div>
        </div>
      ))}
    </div>
  );

  // Render empty state
  const renderEmptyState = () => (
    <div className="text-center py-12">
      <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 className="mt-2 text-sm font-medium text-gray-900">No posts found</h3>
      <p className="mt-1 text-sm text-gray-500">
        Try adjusting your filters or create a new post.
      </p>
      <button
        onClick={clearFilters}
        className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
      >
        Clear Filters
      </button>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-4 bg-gray-50 min-h-screen">
      {/* Search and Filter Bar */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4 items-center">
          {/* Search Bar */}
          <div className="flex-1 w-full md:w-auto">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search posts..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Filter Dropdowns */}
          <div className="flex gap-3">
            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-700"
            >
              <option value="">All Posts</option>
              {categories.map(category => (
                <option key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>

            {/* Sort Filter */}
            <select
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [newSortBy, newSortOrder] = e.target.value.split('-');
                setSortBy(newSortBy);
                setSortOrder(newSortOrder as 'asc' | 'desc');
              }}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-700"
            >
              <option value="created_at-desc">Newest First</option>
              <option value="created_at-asc">Oldest First</option>
              <option value="likes_count-desc">Most Liked</option>
              <option value="views_count-desc">Most Viewed</option>
            </select>
          </div>
        </div>

        {/* Tags Filter */}
        {popularTags.length > 0 && (
          <div className="mt-4">
            <div className="flex flex-wrap gap-2">
              {popularTags.slice(0, 8).map(({ tag, count }) => (
                <button
                  key={tag}
                  onClick={() => handleTagClick(tag)}
                  className={`px-3 py-1 text-sm rounded-full border transition-colors ${
                    selectedTags.includes(tag)
                      ? 'bg-blue-100 border-blue-300 text-blue-800'
                      : 'bg-gray-100 border-gray-300 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  #{tag}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
          <div className="flex">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Posts List */}
      {loading && posts.length === 0 ? (
        renderSkeleton()
      ) : posts.length === 0 ? (
        renderEmptyState()
      ) : (
        <div className="space-y-6">
          {posts.map((post, index) => (
            <div
              key={post.id}
              ref={index === posts.length - 1 ? lastElementRef : null}
              className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow duration-200"
            >
              {/* Post Header */}
              <div className="p-6 pb-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    {/* User Avatar */}
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-lg mr-3">
                      {getUserInitials(post.user || 'User')}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">{post.user || 'Anonymous'}</div>
                      <div className="text-sm text-gray-500">{formatDate(post.created_at)}</div>
                    </div>
                  </div>
                  
                  {/* Options Menu */}
                  <button className="text-gray-400 hover:text-gray-600 p-1">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                </div>

                {/* Post Title */}
                <h3 className="text-xl font-bold text-gray-900 mb-2">{post.title}</h3>

                {/* Post Content */}
                <div
                  className="text-gray-700 mb-4 line-clamp-3"
                  dangerouslySetInnerHTML={{ __html: post.content }}
                />

                {/* Post Image */}
                {post.media_url && (
                  <div className="mb-4">
                    <LazyImage
                      src={`http://localhost:5000${post.media_url}`}
                      alt="Post media"
                      className="w-full rounded-lg"
                      style={{ maxHeight: 400, objectFit: 'cover' }}
                    />
                  </div>
                )}

                {/* Tags */}
                {post.tags && post.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.tags.map((tag, tagIndex) => (
                      <span
                        key={tagIndex}
                        className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full cursor-pointer hover:bg-blue-200 transition-colors"
                        onClick={() => handleTagClick(tag)}
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                  <div className="flex items-center space-x-6">
                    {/* Like Button */}
                    <button
                      onClick={() => handleLike(post.id)}
                      className="flex items-center space-x-2 text-gray-500 hover:text-pink-600 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                      </svg>
                      <span className="text-sm font-medium">{post.likes_count || 0}</span>
                    </button>

                    {/* Comment Button */}
                    <button className="flex items-center space-x-2 text-gray-500 hover:text-blue-600 transition-colors">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                      </svg>
                      <span className="text-sm font-medium">{post.comments_count || 0}</span>
                    </button>

                    {/* Share Button */}
                    <button
                      onClick={() => handleShare(post)}
                      className="flex items-center space-x-2 text-gray-500 hover:text-green-600 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                      </svg>
                      <span className="text-sm font-medium">Share</span>
                    </button>
                  </div>

                  {/* Category Badge */}
                  {post.category && (
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                      {post.category}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}

          {/* Loading indicator for infinite scroll */}
          {(isFetching || loading) && (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          )}

          {/* End of results indicator */}
          {!hasMore && posts.length > 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>You've reached the end of the posts!</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PostListAdvanced;
