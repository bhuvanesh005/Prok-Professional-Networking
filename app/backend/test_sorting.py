#!/usr/bin/env python3

import requests

def test_sorting():
    """Test different sorting options"""
    print("🧪 Testing Sorting Parameters...")
    print("=" * 50)
    
    # Test different sort combinations
    test_cases = [
        ("created_at", "desc", "Newest First"),
        ("created_at", "asc", "Oldest First"),
        ("likes_count", "desc", "Most Liked"),
        ("views_count", "desc", "Most Viewed"),
    ]
    
    for sort_by, sort_order, description in test_cases:
        url = f"http://localhost:5000/api/test/posts?sort_by={sort_by}&sort_order={sort_order}"
        print(f"\n📊 Testing: {description}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {len(data['posts'])} posts returned")
                if data['posts']:
                    first_post = data['posts'][0]
                    print(f"   First post: {first_post.get('title', 'No title')[:50]}...")
                    print(f"   Created: {first_post.get('created_at', 'No date')}")
                    print(f"   Likes: {first_post.get('likes_count', 0)}")
                    print(f"   Views: {first_post.get('views_count', 0)}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_sorting() 