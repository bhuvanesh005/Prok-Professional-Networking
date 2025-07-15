from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from models.user import User
from models.profile import Profile
from models import db
from sqlalchemy import desc
import json

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/api/feed', methods=['GET'])
@jwt_required()
def get_feed():
    """Get the main feed with posts from all users"""
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query posts with user and profile information
        posts = Post.query.join(User).join(Profile).order_by(desc(Post.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        feed_posts = []
        for post in posts.items:
            feed_posts.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'media_url': post.media_url,
                'category': post.category,
                'visibility': post.visibility,
                'tags': post.tags.split(',') if post.tags else [],
                'likes_count': post.likes_count,
                'comments_count': post.comments_count,
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'updated_at': post.updated_at.isoformat() if post.updated_at else None,
                'author': {
                    'id': post.user.id,
                    'name': post.user.username,
                    'avatar_url': post.user.profile.avatar_url if post.user.profile else None,
                    'title': post.user.profile.title if post.user.profile else None
                }
            })
        
        return jsonify({
            'posts': feed_posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': posts.total,
                'pages': posts.pages,
                'has_next': posts.has_next,
                'has_prev': posts.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feed_bp.route('/api/feed/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_feed_by_user(user_id):
    """Get posts from a specific user"""
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query posts from specific user
        posts = Post.query.filter_by(user_id=user_id).join(User).join(Profile).order_by(desc(Post.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        feed_posts = []
        for post in posts.items:
            feed_posts.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'media_url': post.media_url,
                'category': post.category,
                'visibility': post.visibility,
                'tags': post.tags.split(',') if post.tags else [],
                'likes_count': post.likes_count,
                'comments_count': post.comments_count,
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'updated_at': post.updated_at.isoformat() if post.updated_at else None,
                'author': {
                    'id': post.user.id,
                    'name': post.user.username,
                    'avatar_url': post.user.profile.avatar_url if post.user.profile else None,
                    'title': post.user.profile.title if post.user.profile else None
                }
            })
        
        return jsonify({
            'posts': feed_posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': posts.total,
                'pages': posts.pages,
                'has_next': posts.has_next,
                'has_prev': posts.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 