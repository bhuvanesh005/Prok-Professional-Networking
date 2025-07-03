from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.profile import Profile
from models import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not user or not profile:
        return jsonify({'message': 'Profile not found'}), 404
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
        'avatarUrl': '',
        'socialLinks': [],
    })

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
        avatar = files.get('avatar')
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

    # Optionally handle avatar upload (not implemented, just placeholder)
    avatar_url = None
    if avatar:
        # Save avatar to static/uploads and set avatar_url (implement as needed)
        pass

    db.session.commit()
    response = {'message': 'Profile updated successfully'}
    if avatar_url:
        response['avatarUrl'] = avatar_url
    return jsonify(response)