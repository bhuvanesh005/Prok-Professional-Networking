from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from models import db
import os
from werkzeug.utils import secure_filename
import time

posts_bp = Blueprint('posts', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
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

@posts_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@posts_bp.route('/users/<int:user_id>/posts', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200