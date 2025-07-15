# test_posts_endpoint.py
"""
Simple test to verify posts API endpoints work without authentication
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_posts_without_auth():
    """Test posts endpoints without authentication"""
    
    print("🧪 Testing Posts API without authentication...")
    print("=" * 60)
    
    # Test 1: Get posts without auth (using test endpoint)
    print("\n1. Testing GET /api/test/posts (public posts)")
    try:
        response = requests.get(f'{BASE_URL}/api/test/posts?page=1&per_page=5')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            pagination = data.get('pagination', {})
            print(f"✅ Success! Found {len(posts)} posts")
            print(f"📊 Total posts: {pagination.get('total', 0)}")
            print(f"📄 Has next page: {pagination.get('has_next', False)}")
            
            if posts:
                print("\n📝 First post preview:")
                first_post = posts[0]
                print(f"  Title: {first_post.get('title', 'N/A')}")
                print(f"  Author: {first_post.get('user', 'N/A')}")
                print(f"  Category: {first_post.get('category', 'N/A')}")
                print(f"  Likes: {first_post.get('likes_count', 0)}")
                print(f"  Comments: {first_post.get('comments_count', 0)}")
                print(f"  Has image: {'Yes' if first_post.get('media_url') else 'No'}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get categories (using test endpoint)
    print("\n2. Testing GET /api/test/categories")
    try:
        response = requests.get(f'{BASE_URL}/api/test/categories')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            print(f"✅ Success! Found {len(categories)} categories")
            print(f"📋 Categories: {categories}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get popular tags (using test endpoint)
    print("\n3. Testing GET /api/test/popular-tags")
    try:
        response = requests.get(f'{BASE_URL}/api/test/popular-tags?limit=10')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            tags = data.get('tags', [])
            print(f"✅ Success! Found {len(tags)} popular tags")
            if tags:
                print(f"🏷️  Top tags: {[tag['tag'] for tag in tags[:5]]}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Search posts (using test endpoint)
    print("\n4. Testing GET /api/test/posts with search")
    try:
        response = requests.get(f'{BASE_URL}/api/test/posts?search=react&page=1&per_page=3')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            print(f"✅ Success! Found {len(posts)} posts with 'react' search")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Posts API testing completed!")

if __name__ == '__main__':
    test_posts_without_auth() 