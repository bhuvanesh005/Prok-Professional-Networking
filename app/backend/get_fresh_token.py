#!/usr/bin/env python3

import requests
import json

def get_fresh_token():
    """Get a fresh JWT token by logging in"""
    print("🔑 Getting Fresh JWT Token...")
    print("=" * 50)
    
    # Login data
    login_data = {
        "username": "Bhuvan",
        "password": "password123"
    }
    
    try:
        # Login to get fresh token
        response = requests.post('http://localhost:5000/api/login', json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✅ Login successful!")
            print(f"Token: {token[:50]}...")
            print(f"\n🔧 To use this token in your browser:")
            print(f"1. Open browser developer tools (F12)")
            print(f"2. Go to Console tab")
            print(f"3. Run: localStorage.setItem('token', '{token}')")
            print(f"4. Refresh the page")
            print(f"\nOr copy this command:")
            print(f"localStorage.setItem('token', '{token}')")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_fresh_token() 