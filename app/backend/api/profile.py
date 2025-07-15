from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.profile import Profile
from models import db
import os
from werkzeug.utils import secure_filename
from PIL import Image
import time
import magic

profile_bp = Blueprint('profile', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    # Check file type
    file.seek(0)
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if mime not in ['image/jpeg', 'image/png']:
        return False
    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return False
    return True

@profile_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        profile = Profile.query.filter_by(user_id=user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        if not profile:
            return jsonify({'message': 'Profile not found for user'}), 404
            
        # Fetch skills as array
        from models.profile import Skill, Experience, Education, Activity
        skills = [s.name for s in Skill.query.filter_by(profile_id=profile.id).all()]
        # Fetch languages as array (store as comma-separated in profile.languages)
        languages = (profile.languages or '').split(',') if hasattr(profile, 'languages') else []
        # Fetch experience as list of dicts
        experience = [
            {
                'company': e.company,
                'title': e.title,
                'start': str(e.start_date) if e.start_date else '',
                'end': str(e.end_date) if e.end_date else '',
            }
            for e in Experience.query.filter_by(profile_id=profile.id).all()
        ]
        # Fetch education as list of dicts
        education = [
            {
                'school': ed.school,
                'degree': ed.degree,
                'start': str(ed.start_year) if ed.start_year else '',
                'end': str(ed.end_year) if ed.end_year else '',
            }
            for ed in Education.query.filter_by(profile_id=profile.id).all()
        ]
        # Fetch activity as list of dicts
        activity = [
            {
                'type': a.type,
                'content': a.content,
                'date': a.date,
            }
            for a in Activity.query.filter_by(profile_id=profile.id).order_by(Activity.id.desc()).all()
        ]
        return jsonify({
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'title': getattr(profile, 'title', ''),
            'bio': profile.bio,
            'location': profile.location,
            'skills': skills,
            'languages': languages,
            'experience': experience,
            'education': education,
            'contact': {'email': user.email, 'phone': getattr(profile, 'phone', '')},
            'activity': activity,
            'connections': getattr(profile, 'connections', 0),
            'mutualConnections': getattr(profile, 'mutualConnections', 0),
            'avatarUrl': profile.avatar_url or '',
            'socialLinks': [],
        })
    except Exception as e:
        return jsonify({'message': f'Error fetching profile: {str(e)}'}), 500

@profile_bp.route('/api/profile/test', methods=['GET'])
def get_profile_test():
    """Test endpoint that bypasses authentication for debugging"""
    try:
        # Get the first user and profile for testing
        user = User.query.first()
        if not user:
            return jsonify({'message': 'No users found in database'}), 404
            
        profile = Profile.query.filter_by(user_id=user.id).first()
        if not profile:
            return jsonify({'message': 'No profile found for first user'}), 404
            
        # Fetch skills as array
        from models.profile import Skill, Experience, Education, Activity
        skills = [s.name for s in Skill.query.filter_by(profile_id=profile.id).all()]
        # Fetch languages as array (store as comma-separated in profile.languages)
        languages = (profile.languages or '').split(',') if hasattr(profile, 'languages') else []
        # Fetch experience as list of dicts
        experience = [
            {
                'company': e.company,
                'title': e.title,
                'start': str(e.start_date) if e.start_date else '',
                'end': str(e.end_date) if e.end_date else '',
            }
            for e in Experience.query.filter_by(profile_id=profile.id).all()
        ]
        # Fetch education as list of dicts
        education = [
            {
                'school': ed.school,
                'degree': ed.degree,
                'start': str(ed.start_year) if ed.start_year else '',
                'end': str(ed.end_year) if ed.end_year else '',
            }
            for ed in Education.query.filter_by(profile_id=profile.id).all()
        ]
        # Fetch activity as list of dicts
        activity = [
            {
                'type': a.type,
                'content': a.content,
                'date': a.date,
            }
            for a in Activity.query.filter_by(profile_id=profile.id).order_by(Activity.id.desc()).all()
        ]
        
        return jsonify({
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'title': getattr(profile, 'title', ''),
            'bio': profile.bio,
            'location': profile.location,
            'skills': skills,
            'languages': languages,
            'experience': experience,
            'education': education,
            'contact': {'email': user.email, 'phone': getattr(profile, 'phone', '')},
            'activity': activity,
            'connections': getattr(profile, 'connections', 0),
            'mutualConnections': getattr(profile, 'mutualConnections', 0),
            'avatarUrl': profile.avatar_url or '',
            'socialLinks': [],
        })
    except Exception as e:
        return jsonify({'message': f'Error fetching profile: {str(e)}'}), 500

@profile_bp.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not user or not profile:
        return jsonify({'message': 'Profile not found'}), 404

    # Handle both JSON and multipart/form-data
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        form = request.form
        files = request.files
        name = form.get('name')
        email = form.get('email')
        bio = form.get('bio')
        title = form.get('title')
        skills_raw = form.get('skills')
        languages_raw = form.get('languages')
        connections = form.get('connections')
        mutualConnections = form.get('mutualConnections')
        phone = form.get('phone')
        location = form.get('location')
        # Parse skills as JSON array if present
        import json
        try:
            skills = json.loads(skills_raw) if skills_raw else []
        except Exception:
            skills = []
        try:
            languages = json.loads(languages_raw) if languages_raw else []
        except Exception:
            languages = []
    else:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        bio = data.get('bio')
        title = data.get('title')
        skills = data.get('skills', [])
        languages = data.get('languages', [])
        connections = data.get('connections')
        mutualConnections = data.get('mutualConnections')
        avatar = None
        phone = data.get('contact', {}).get('phone')
        location = data.get('location')
        education = data.get('education', [])
        activity = data.get('activity', [])

    if name:
        user.username = name
    if email:
        user.email = email
    if bio is not None:
        profile.bio = bio
    if title is not None:
        profile.title = title
    if languages is not None and hasattr(profile, 'languages'):
        profile.languages = ','.join(languages)
    if connections is not None and hasattr(profile, 'connections'):
        try:
            profile.connections = int(connections)
        except Exception:
            profile.connections = 0
    if mutualConnections is not None and hasattr(profile, 'mutualConnections'):
        try:
            profile.mutualConnections = int(mutualConnections)
        except Exception:
            profile.mutualConnections = 0
    if phone is not None and hasattr(profile, 'phone'):
        profile.phone = phone
    if location is not None:
        profile.location = location

    # Update skills (replace all for simplicity)
    from models.profile import Skill
    if skills is not None:
        Skill.query.filter_by(profile_id=profile.id).delete()
        for skill_name in skills:
            if skill_name:
                db.session.add(Skill(profile_id=profile.id, name=skill_name))

    # Update education (replace all for simplicity)
    from models.profile import Education
    if education is not None:
        Education.query.filter_by(profile_id=profile.id).delete()
        for edu in education:
            if edu.get('school') or edu.get('degree'):
                db.session.add(Education(
                    profile_id=profile.id,
                    school=edu.get('school', ''),
                    degree=edu.get('degree', ''),
                    start_year=edu.get('start', None),
                    end_year=edu.get('end', None)
                ))

    # Update activity (replace all for simplicity)
    from models.profile import Activity
    if activity is not None:
        Activity.query.filter_by(profile_id=profile.id).delete()
        for act in activity:
            if act.get('type') or act.get('content'):
                db.session.add(Activity(
                    profile_id=profile.id,
                    type=act.get('type', ''),
                    content=act.get('content', ''),
                    date=act.get('date', '')
                ))

    db.session.commit()
    response = {'message': 'Profile updated successfully'}
    if profile.avatar_url:
        response['avatarUrl'] = profile.avatar_url
    return jsonify(response)

@profile_bp.route('/api/profile/image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not user or not profile:
        return jsonify({'message': 'Profile not found'}), 404
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if not allowed_file(file.filename) or not validate_image(file):
        return jsonify({'message': 'Invalid file type or size'}), 400
    # Secure file naming
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"profile_{user_id}_{int(time.time())}.{ext}"
    filename = secure_filename(filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    # Image processing: compression, resizing, thumbnail, format conversion
    image = Image.open(file)
    image = image.convert('RGB')
    image.thumbnail((400, 400))  # Resize
    image.save(filepath, format='JPEG', quality=85, optimize=True)  # Compression
    # Optionally, generate thumbnail
    thumb_path = os.path.join(UPLOAD_FOLDER, f"thumb_{filename}")
    image.thumbnail((100, 100))
    image.save(thumb_path, format='JPEG', quality=70, optimize=True)
    # Update profile with image URL (relative path)
    profile.avatar_url = f"/static/uploads/{filename}"
    db.session.commit()
    return jsonify({'imageUrl': profile.avatar_url}), 200

# Serve uploaded profile images
@profile_bp.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../static/uploads'), filename)