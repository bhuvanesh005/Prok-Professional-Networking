-- Migration to add new features to posts table
-- Run this migration to add the new columns for advanced post listing

-- Add new columns to posts table
ALTER TABLE posts ADD COLUMN IF NOT EXISTS category VARCHAR(100) DEFAULT 'general';
ALTER TABLE posts ADD COLUMN IF NOT EXISTS tags TEXT;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS visibility VARCHAR(20) DEFAULT 'public';
ALTER TABLE posts ADD COLUMN IF NOT EXISTS likes_count INTEGER DEFAULT 0;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS views_count INTEGER DEFAULT 0;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS comments_count INTEGER DEFAULT 0;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_post_created_at ON posts(created_at);
CREATE INDEX IF NOT EXISTS idx_post_category ON posts(category);
CREATE INDEX IF NOT EXISTS idx_post_visibility ON posts(visibility);
CREATE INDEX IF NOT EXISTS idx_post_likes_count ON posts(likes_count);
CREATE INDEX IF NOT EXISTS idx_post_views_count ON posts(views_count);
CREATE INDEX IF NOT EXISTS idx_post_user_id ON posts(user_id);

-- Add trigger to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_posts_updated_at ON posts;
CREATE TRIGGER update_posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Update existing posts to have default values
UPDATE posts SET 
    category = 'general',
    visibility = 'public',
    likes_count = 0,
    views_count = 0,
    comments_count = 0,
    updated_at = created_at
WHERE category IS NULL OR visibility IS NULL;
