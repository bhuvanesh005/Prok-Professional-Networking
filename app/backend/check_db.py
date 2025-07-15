#!/usr/bin/env python3

from main import app
from models import db
from models.user import User
from models.profile import Profile
import requests

def check_database():
    with app.app_context():
        print("🔍 Checking Database Contents...")
        print("=" * 50)
        
        user_count = User.query.count()
        profile_count = Profile.query.count()
        
        print(f"Users in database: {user_count}")
        print(f"Profiles in database: {profile_count}")
        
        if user_count > 0:
            users = User.query.all()
            print(f"User IDs: {[u.id for u in users]}")
            print(f"Usernames: {[u.username for u in users]}")
        
        if profile_count > 0:
            profiles = Profile.query.all()
            print(f"Profile user IDs: {[p.user_id for p in profiles]}")
        
        print("\n" + "=" * 50)

def test_profile_endpoint():
    print("🧪 Testing Profile Endpoint...")
    print("=" * 50)
    
    try:
        # Test the new test endpoint
        response = requests.get('http://localhost:5000/api/profile/test')
        print(f"Test endpoint status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Profile found for user: {data.get('name', 'Unknown')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

if __name__ == "__main__":
    check_database()
    test_profile_endpoint() 