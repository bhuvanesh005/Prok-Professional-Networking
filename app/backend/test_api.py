# test_api.py
"""
Simple test script to verify the posts API endpoints are working correctly.
Run this after starting the Flask server to test the API functionality.
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_posts_api():
    """Test the posts API endpoints"""
    
    print("🧪 Testing Posts API Endpoints...")
    print("=" * 50)
    
    # Test 1: Get categories
    print("\n1. Testing GET /api/posts/categories")
    try:
        response = requests.get(f'{BASE_URL}/api/posts/categories', 
                              headers={'Authorization': 'Bearer test'})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Categories: {data.get('categories', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Get popular tags
    print("\n2. Testing GET /api/posts/popular-tags")
    try:
        response = requests.get(f'{BASE_URL}/api/posts/popular-tags?limit=10', 
                              headers={'Authorization': 'Bearer test'})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Popular tags: {data.get('tags', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get posts with basic filtering
    print("\n3. Testing GET /api/posts")
    try:
        response = requests.get(f'{BASE_URL}/api/posts?page=1&per_page=5', 
                              headers={'Authorization': 'Bearer test'})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            pagination = data.get('pagination', {})
            print(f"Posts returned: {len(posts)}")
            print(f"Total posts: {pagination.get('total', 0)}")
            print(f"Has next page: {pagination.get('has_next', False)}")
            
            if posts:
                print("\nFirst post preview:")
                first_post = posts[0]
                print(f"  Title: {first_post.get('title', 'N/A')}")
                print(f"  Category: {first_post.get('category', 'N/A')}")
                print(f"  Tags: {first_post.get('tags', [])}")
                print(f"  Views: {first_post.get('views_count', 0)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Get posts with search filter
    print("\n4. Testing GET /api/posts with search filter")
    try:
        response = requests.get(f'{BASE_URL}/api/posts?search=react&page=1&per_page=3', 
                              headers={'Authorization': 'Bearer test'})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            print(f"Posts found with 'react' search: {len(posts)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Get posts with category filter
    print("\n5. Testing GET /api/posts with category filter")
    try:
        response = requests.get(f'{BASE_URL}/api/posts?category=technology&page=1&per_page=3', 
                              headers={'Authorization': 'Bearer test'})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            print(f"Posts found in 'technology' category: {len(posts)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Get posts with sorting
    print("\n6. Testing GET /api/posts with sorting")
    try:
        response = requests.get(f'{BASE_URL}/api/posts?sort_by=likes_count&sort_order=desc&page=1&per_page=3', 
                              headers={'Authorization': 'Bearer test'})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            print(f"Posts sorted by likes (desc): {len(posts)}")
            if posts:
                print(f"Highest likes: {posts[0].get('likes_count', 0)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")

if __name__ == '__main__':
    test_posts_api() 