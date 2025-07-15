from flask import Blueprint, request, jsonify
from models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token  # <-- Add this import
from models.profile import Profile  # <-- Add this import
import datetime
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'Username or email already exists'}), 400
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    # Create a profile for the new user
    profile = Profile(user_id=user.id, bio='', location='')
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    username_or_email = data.get('username')
    password = data.get('password')
    print(f"[DEBUG] Login attempt: username_or_email={username_or_email}")
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    print(f"[DEBUG] User found: {user is not None}")
    if user:
        print(f"[DEBUG] Password check: {user.check_password(password)}")
    if not user or not user.check_password(password):
        print("[DEBUG] Invalid credentials")
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user.id))  # <-- Use string for identity
    return jsonify({'token': access_token, 'user': user.to_dict()}), 200