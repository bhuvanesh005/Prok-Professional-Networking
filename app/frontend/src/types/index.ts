export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export interface Profile {
  id: number;
  user_id: number;
  name: string;
  email: string;
  bio: string;
  location: string;
  skills: string[];
  experience: Experience[];
  education: Education[];
}

export interface Experience {
  id: number;
  title: string;
  company: string;
  start_date: string;
  end_date: string;
  description: string;
}

export interface Education {
  id: number;
  school: string;
  degree: string;
  field: string;
  start_date: string;
  end_date: string;
}

export interface Post {
  id: number;
  user_id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at?: string;
  category?: string;
  tags?: string[];
  visibility?: 'public' | 'private' | 'connections';
  likes_count?: number;
  views_count?: number;
  comments_count?: number;
  likes?: number; // Keep for backward compatibility
  comments?: Comment[];
  user?: string;
  media_url?: string;
}

export interface PostsResponse {
  posts: Post[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
    next_num: number | null;
    prev_num: number | null;
  };
}

export interface PostFilters {
  search?: string;
  category?: string;
  visibility?: string;
  tags?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  page?: number;
  per_page?: number;
}

export interface PopularTag {
  tag: string;
  count: number;
}

export interface Comment {
  id: number;
  user_id: number;
  content: string;
  created_at: string;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements: string[];
  created_at: string;
}

export interface Message {
  id: number;
  sender_id: number;
  receiver_id: number;
  content: string;
  created_at: string;
  read: boolean;
}
