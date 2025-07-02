from flask import Blueprint, request, jsonify
from models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
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
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
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
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token, 'user': user.to_dict()}), 200