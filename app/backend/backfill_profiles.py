# backfill_profiles.py
"""
Script to backfill missing Profile rows for all existing users.
Run this once after updating your models to ensure all users have a profile.
"""
from models import user as user_model, profile as profile_model
from main import db, app

with app.app_context():
    User = user_model.User
    Profile = profile_model.Profile

    users = User.query.all()
    count = 0
    for user in users:
        if not Profile.query.filter_by(user_id=user.id).first():
            profile = Profile(user_id=user.id, bio='', location='')
            db.session.add(profile)
            count += 1
    db.session.commit()
    print(f"Backfilled {count} missing profiles.")
