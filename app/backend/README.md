# Backend Setup

## Prerequisites
- Python 3.8+
- MySQL 8.0+
- Virtual environment (recommended)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
Make sure MySQL is running and create the database:
```bash
mysql -u root -p
CREATE DATABASE prok_db;
```

### 3. Run Migrations
If you need to add new columns to existing tables:
```bash
python run_migrations.py
```

### 4. Start the Server
```bash
python main.py
```

The server will run on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/signup` - User registration

### Posts
- `GET /api/posts` - Get posts with filtering and pagination
- `POST /api/posts` - Create a new post
- `GET /api/posts/categories` - Get all categories
- `GET /api/posts/popular-tags` - Get popular tags
- `POST /api/posts/<id>/like` - Like a post
- `GET /users/<id>/posts` - Get user's posts

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

## Database Schema

### Posts Table
- `id` - Primary key
- `title` - Post title
- `content` - Post content (HTML)
- `media_url` - Media file URL
- `user_id` - Foreign key to users table
- `category` - Post category
- `tags` - JSON string of tags
- `visibility` - Post visibility (public/private/connections)
- `likes_count` - Number of likes
- `views_count` - Number of views
- `comments_count` - Number of comments
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Troubleshooting

### Database Connection Issues
- Check if MySQL is running
- Verify database credentials in `config.py`
- Ensure database `prok_db` exists

### Missing Columns Error
If you get "Unknown column" errors, run:
```bash
python run_migrations.py
```

### Port Already in Use
If port 5000 is busy, change it in `main.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
``` 