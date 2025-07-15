# debug_profile.py
"""
Debug script to check profile authentication issue
"""
from main import app
from models import db
from models.profile import Profile
from models.user import User
from flask_jwt_extended import decode_token

def debug_profile_issue():
    """Debug the profile not found issue"""
    
    with app.app_context():
        # Test token from the error
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjU1MjQ3NywianRpIjoiNWYyNjBmZTYtNTg2ZS00ZjNhLTg1ZDAtMDg1MzFhYWU1NzQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTI1NTI0NzcsImV4cCI6MTc1MjU1NjA3N30.cS6gBeQ-WNCX-4sW_094-bDmW6HuJD41OFIylC63ZMs'
        
        try:
            print("🔍 Debugging Profile Issue...")
            print("=" * 50)
            
            # Decode the token
            decoded = decode_token(token)
            user_id = int(decoded['sub'])
            print(f"✅ Token decoded successfully")
            print(f"📋 User ID from token: {user_id}")
            
            # Check if user exists
            user = User.query.get(user_id)
            print(f"👤 User found: {user is not None}")
            if user:
                print(f"   Username: {user.username}")
                print(f"   Email: {user.email}")
            
            # Check if profile exists
            profile = Profile.query.filter_by(user_id=user_id).first()
            print(f"📄 Profile found: {profile is not None}")
            if profile:
                print(f"   Bio: {profile.bio}")
                print(f"   Location: {profile.location}")
                print(f"   Title: {getattr(profile, 'title', 'N/A')}")
            
            # Check all users and profiles
            print(f"\n📊 Database Summary:")
            print(f"   Total users: {User.query.count()}")
            print(f"   Total profiles: {Profile.query.count()}")
            
            # List all users and their profiles
            users = User.query.all()
            for u in users:
                p = Profile.query.filter_by(user_id=u.id).first()
                print(f"   User {u.id}: {u.username} - Profile: {'Yes' if p else 'No'}")
            
            # Check if the issue is in the profile API logic
            if user and profile:
                print(f"\n✅ Both user and profile exist - API should work")
                print(f"❌ The issue might be in the API endpoint logic")
            elif user and not profile:
                print(f"\n❌ User exists but no profile - need to create profile")
            elif not user:
                print(f"\n❌ User not found - authentication issue")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    debug_profile_issue() 