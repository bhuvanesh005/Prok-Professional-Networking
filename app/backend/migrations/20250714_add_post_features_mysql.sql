-- Migration to add new features to posts table (MySQL version)
-- Run this migration to add the new columns for advanced post listing

-- Add new columns to posts table (MySQL doesn't support IF NOT EXISTS for ADD COLUMN)
-- We'll add them one by one and handle errors gracefully

-- Add category column
ALTER TABLE posts ADD COLUMN category VARCHAR(100) DEFAULT 'general';

-- Add tags column  
ALTER TABLE posts ADD COLUMN tags TEXT;

-- Add visibility column
ALTER TABLE posts ADD COLUMN visibility VARCHAR(20) DEFAULT 'public';

-- Add likes_count column
ALTER TABLE posts ADD COLUMN likes_count INT DEFAULT 0;

-- Add views_count column
ALTER TABLE posts ADD COLUMN views_count INT DEFAULT 0;

-- Add comments_count column
ALTER TABLE posts ADD COLUMN comments_count INT DEFAULT 0;

-- Add updated_at column
ALTER TABLE posts ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Create indexes for better query performance
CREATE INDEX idx_post_created_at ON posts(created_at);
CREATE INDEX idx_post_category ON posts(category);
CREATE INDEX idx_post_visibility ON posts(visibility);
CREATE INDEX idx_post_likes_count ON posts(likes_count);
CREATE INDEX idx_post_views_count ON posts(views_count);
CREATE INDEX idx_post_user_id ON posts(user_id);

-- Update existing posts to have default values
UPDATE posts SET 
    category = 'general',
    visibility = 'public',
    likes_count = 0,
    views_count = 0,
    comments_count = 0,
    updated_at = created_at
WHERE category IS NULL OR visibility IS NULL; 