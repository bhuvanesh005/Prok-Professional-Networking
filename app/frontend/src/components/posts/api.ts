import type { PostFilters, PostsResponse, PopularTag } from '../../types';

const API_URL = 'http://localhost:5000';

export const postsApi = {
  createPost: async (title: string, content: string, media?: File) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    if (media) {
      formData.append('media', media);
    }

    const response = await fetch(`${API_URL}/api/posts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: formData,
    });
    return response.json();
  },

  getPosts: async (filters: PostFilters = {}): Promise<PostsResponse> => {
    const params = new URLSearchParams();
    
    // Add filters to query parameters
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });

    // Use test endpoint for now to bypass authentication
    const response = await fetch(`${API_URL}/api/test/posts?${params.toString()}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch posts: ${response.statusText}`);
    }
    
    return response.json();
  },

  getCategories: async (): Promise<{ categories: string[] }> => {
    // Use test endpoint for now to bypass authentication
    const response = await fetch(`${API_URL}/api/test/categories`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch categories: ${response.statusText}`);
    }
    
    return response.json();
  },

  getPopularTags: async (limit: number = 50): Promise<{ tags: PopularTag[] }> => {
    // Use test endpoint for now to bypass authentication
    const response = await fetch(`${API_URL}/api/test/popular-tags?limit=${limit}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch popular tags: ${response.statusText}`);
    }
    
    return response.json();
  },

  likePost: async (postId: number) => {
    const response = await fetch(`${API_URL}/api/posts/${postId}/like`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.json();
  },

  getPostsByUser: async (userId: number) => {
    const response = await fetch(`${API_URL}/api/users/${userId}/posts`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.json();
  },
};
