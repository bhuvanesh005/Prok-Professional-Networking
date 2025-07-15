from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from models import db
from sqlalchemy import or_, and_, desc, asc, func
import os
from werkzeug.utils import secure_filename
import time
import json
from functools import lru_cache

posts_bp = Blueprint('posts', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Cache for frequently accessed data
@lru_cache(maxsize=128)
def get_cached_categories():
    """Get all available categories with caching"""
    categories = db.session.query(Post.category).filter(Post.category.isnot(None)).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@lru_cache(maxsize=128)
def get_cached_popular_tags(limit=50):
    """Get most popular tags with caching"""
    posts_with_tags = Post.query.filter(Post.tags.isnot(None)).all()
    tag_counts = {}
    
    for post in posts_with_tags:
        try:
            tags = json.loads(post.tags)
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        except:
            continue
    
    # Sort by count and return top tags
    popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{'tag': tag, 'count': count} for tag, count in popular_tags]

# Test endpoint without authentication
@posts_bp.route('/api/test/posts', methods=['GET'])
def test_get_posts():
    """Test endpoint to get posts without authentication"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        
        # Start with base query for public posts only
        query = Post.query.filter(Post.visibility == 'public')
        
        # Apply search filter
        if search:
            search_filter = or_(
                Post.title.ilike(f'%{search}%'),
                Post.content.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Apply category filter
        if category:
            query = query.filter(Post.category == category)
        
        # Apply sorting
        query = query.order_by(desc(Post.created_at))
        
        # Execute pagination
        paginated_posts = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in paginated_posts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated_posts.total,
                'pages': paginated_posts.pages,
                'has_next': paginated_posts.has_next,
                'has_prev': paginated_posts.has_prev,
                'next_num': paginated_posts.next_num,
                'prev_num': paginated_posts.prev_num
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching posts: {str(e)}'}), 500

@posts_bp.route('/api/test/categories', methods=['GET'])
def test_get_categories():
    """Test endpoint to get categories without authentication"""
    try:
        categories = get_cached_categories()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching categories: {str(e)}'}), 500

@posts_bp.route('/api/test/popular-tags', methods=['GET'])
def test_get_popular_tags():
    """Test endpoint to get popular tags without authentication"""
    try:
        limit = request.args.get('limit', 50, type=int)
        popular_tags = get_cached_popular_tags(limit)
        return jsonify({'tags': popular_tags}), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching popular tags: {str(e)}'}), 500

@posts_bp.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    
    # Handle both JSON and form data
    if request.content_type and 'application/json' in request.content_type:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        media_file = None
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        media_file = request.files.get('media')

    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400

    media_url = None
    if media_file:
        if not allowed_file(media_file.filename):
            return jsonify({'message': 'Invalid file type'}), 400
        
        media_file.seek(0, os.SEEK_END)
        file_length = media_file.tell()
        if file_length > MAX_FILE_SIZE:
            return jsonify({'message': 'File size exceeds the 16MB limit'}), 400
        media_file.seek(0)

        ext = media_file.filename.rsplit('.', 1)[1].lower()
        filename = f"post_{user_id}_{int(time.time())}.{ext}"
        filename = secure_filename(filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        media_file.save(filepath)
        media_url = f"/static/uploads/{filename}"

    new_post = Post(title=title, content=content, media_url=media_url, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201

@posts_bp.route('/api/posts', methods=['GET'])
@jwt_required()
def get_posts():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)  # Max 50 per page
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    visibility = request.args.get('visibility', '').strip()
    tags = request.args.get('tags', '').strip()
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Start with base query
    query = Post.query
    
    # Apply search filter
    if search:
        search_filter = or_(
            Post.title.ilike(f'%{search}%'),
            Post.content.ilike(f'%{search}%')
        )
        query = query.filter(search_filter)
    
    # Apply category filter
    if category:
        query = query.filter(Post.category == category)
    
    # Apply visibility filter
    if visibility:
        query = query.filter(Post.visibility == visibility)
    else:
        # Default to public posts only
        query = query.filter(Post.visibility == 'public')
    
    # Apply tags filter
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        if tag_list:
            tag_filters = []
            for tag in tag_list:
                tag_filters.append(Post.tags.ilike(f'%"{tag}"%'))
            query = query.filter(or_(*tag_filters))
    
    # Apply sorting
    sort_column = getattr(Post, sort_by, Post.created_at)
    if sort_order.lower() == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Execute pagination
    try:
        paginated_posts = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Increment view count for returned posts
        for post in paginated_posts.items:
            post.views_count = (post.views_count or 0) + 1
        db.session.commit()
        
        return jsonify({
            'posts': [post.to_dict() for post in paginated_posts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated_posts.total,
                'pages': paginated_posts.pages,
                'has_next': paginated_posts.has_next,
                'has_prev': paginated_posts.has_prev,
                'next_num': paginated_posts.next_num,
                'prev_num': paginated_posts.prev_num
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching posts: {str(e)}'}), 500

@posts_bp.route('/api/users/<int:user_id>/posts', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@posts_bp.route('/api/posts/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all available post categories"""
    try:
        categories = get_cached_categories()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching categories: {str(e)}'}), 500

@posts_bp.route('/api/posts/popular-tags', methods=['GET'])
@jwt_required()
def get_popular_tags():
    """Get most popular tags"""
    try:
        limit = request.args.get('limit', 50, type=int)
        popular_tags = get_cached_popular_tags(limit)
        return jsonify({'tags': popular_tags}), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching popular tags: {str(e)}'}), 500

@posts_bp.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    """Like or unlike a post"""
    user_id = get_jwt_identity()
    
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check if user already liked the post
        # For now, we'll just increment the likes count
        # In a real implementation, you'd have a separate likes table
        post.likes_count = (post.likes_count or 0) + 1
        db.session.commit()
        
        return jsonify({
            'message': 'Post liked successfully',
            'likes_count': post.likes_count
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error liking post: {str(e)}'}), 500

# Cache invalidation functions
def invalidate_cache():
    """Invalidate all caches when posts are modified"""
    get_cached_categories.cache_clear()
    get_cached_popular_tags.cache_clear()

# Update create_post to invalidate cache
@posts_bp.after_request
def after_request(response):
    """Invalidate cache after POST requests"""
    if request.method == 'POST' and request.endpoint in ['posts.create_post', 'posts.like_post']:
        invalidate_cache()
    return response
