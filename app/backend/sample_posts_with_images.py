# sample_posts_with_images.py
"""
Script to create sample posts with realistic images for testing the posts listing functionality.
This creates posts that look more like the screenshot with proper images and content.
"""
import json
import requests
import os
from models import db
from models.post import Post
from models.user import User
from main import app

def download_image(url, filename):
    """Download an image from URL and save it locally"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return f"/static/uploads/{filename}"
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
    return None

def create_sample_posts_with_images():
    """Create sample posts with realistic images and content"""
    
    with app.app_context():
        # Get the first user (or create one if none exists)
        user = User.query.first()
        if not user:
            print("No users found. Please create a user first.")
            return
        
        # Sample posts with realistic content and images
        sample_posts = [
            {
                'title': 'Post Title 5',
                'content': '<p>This is the content of post 5. It contains some sample text to demonstrate the layout and styling of the post list component. The content is designed to show how the cards will look with real data.</p>',
                'category': 'technology',
                'tags': ['react', 'javascript', 'frontend'],
                'visibility': 'public',
                'likes_count': 249,
                'views_count': 1200,
                'comments_count': 73,
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=400&fit=crop',
                'image_filename': 'post_5_diver.jpg'
            },
            {
                'title': 'Post Title 6',
                'content': '<p>This is the content of post 6. It contains some sample text to demonstrate the layout and styling of the post list component. This post shows how cards look without images.</p>',
                'category': 'programming',
                'tags': ['python', 'backend', 'api'],
                'visibility': 'public',
                'likes_count': 326,
                'views_count': 890,
                'comments_count': 62,
                'image_url': None,
                'image_filename': None
            },
            {
                'title': 'Post Title 7',
                'content': '<p>This is the content of post 7. It contains some sample text to demonstrate the layout and styling of the post list component. Another example of a text-only post.</p>',
                'category': 'career',
                'tags': ['career', 'development', 'growth'],
                'visibility': 'public',
                'likes_count': 426,
                'views_count': 1100,
                'comments_count': 47,
                'image_url': None,
                'image_filename': None
            },
            {
                'title': 'Getting Started with React Development',
                'content': '<p>React is a powerful JavaScript library for building user interfaces. In this comprehensive guide, I\'ll share everything you need to know to get started with React development.</p><p>Key topics covered:</p><ul><li>Component-based architecture</li><li>State management</li><li>Props and data flow</li><li>Hooks and functional components</li></ul>',
                'category': 'technology',
                'tags': ['react', 'javascript', 'frontend', 'web-development'],
                'visibility': 'public',
                'likes_count': 156,
                'views_count': 2340,
                'comments_count': 89,
                'image_url': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&h=400&fit=crop',
                'image_filename': 'post_react_dev.jpg'
            },
            {
                'title': 'Python Best Practices for Backend Development',
                'content': '<p>Python has become the go-to language for backend development. Here are the essential best practices I\'ve learned over years of building scalable applications.</p><p>We\'ll cover:</p><ul><li>Code organization and structure</li><li>Error handling strategies</li><li>Performance optimization</li><li>Security considerations</li></ul>',
                'category': 'programming',
                'tags': ['python', 'backend', 'best-practices', 'api'],
                'visibility': 'public',
                'likes_count': 234,
                'views_count': 1890,
                'comments_count': 67,
                'image_url': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&h=400&fit=crop',
                'image_filename': 'post_python_backend.jpg'
            },
            {
                'title': 'Career Tips for Software Engineers',
                'content': '<p>Building a successful career in software engineering requires more than just technical skills. Here are the insights that helped me grow from junior developer to senior engineer.</p><p>Important aspects to focus on:</p><ul><li>Continuous learning and skill development</li><li>Networking and community involvement</li><li>Soft skills and communication</li><li>Work-life balance and mental health</li></ul>',
                'category': 'career',
                'tags': ['career', 'software-engineering', 'professional-development'],
                'visibility': 'public',
                'likes_count': 189,
                'views_count': 1450,
                'comments_count': 34,
                'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=400&fit=crop',
                'image_filename': 'post_career_tips.jpg'
            },
            {
                'title': 'Machine Learning Fundamentals',
                'content': '<p>Machine learning is transforming industries across the globe. Let\'s explore the fundamental concepts that every developer should understand.</p><p>Core concepts we\'ll cover:</p><ul><li>Supervised vs Unsupervised Learning</li><li>Feature Engineering and Selection</li><li>Model Evaluation and Validation</li><li>Overfitting Prevention Techniques</li></ul>',
                'category': 'ai-ml',
                'tags': ['machine-learning', 'ai', 'data-science', 'algorithms'],
                'visibility': 'public',
                'likes_count': 312,
                'views_count': 2670,
                'comments_count': 123,
                'image_url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop',
                'image_filename': 'post_ml_fundamentals.jpg'
            },
            {
                'title': 'Web Security Best Practices',
                'content': '<p>Security should be a top priority in web development. Here are the essential practices to protect your applications from common vulnerabilities.</p><p>Key security areas:</p><ul><li>Input validation and sanitization</li><li>Authentication and authorization</li><li>Data encryption and protection</li><li>Regular security audits and testing</li></ul>',
                'category': 'security',
                'tags': ['security', 'web-development', 'authentication', 'encryption'],
                'visibility': 'public',
                'likes_count': 198,
                'views_count': 1780,
                'comments_count': 56,
                'image_url': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&h=400&fit=crop',
                'image_filename': 'post_web_security.jpg'
            }
        ]
        
        # Create posts
        created_count = 0
        for post_data in sample_posts:
            # Check if post already exists (by title)
            existing_post = Post.query.filter_by(title=post_data['title']).first()
            if not existing_post:
                # Download image if provided
                media_url = None
                if post_data['image_url']:
                    media_url = download_image(post_data['image_url'], post_data['image_filename'])
                
                post = Post(
                    title=post_data['title'],
                    content=post_data['content'],
                    category=post_data['category'],
                    tags=json.dumps(post_data['tags']),
                    visibility=post_data['visibility'],
                    likes_count=post_data['likes_count'],
                    views_count=post_data['views_count'],
                    comments_count=post_data['comments_count'],
                    media_url=media_url,
                    user_id=user.id
                )
                db.session.add(post)
                created_count += 1
        
        db.session.commit()
        print(f"✅ Created {created_count} sample posts with images successfully!")
        print(f"📊 Total posts in database: {Post.query.count()}")
        print(f"🖼️  Posts with images: {Post.query.filter(Post.media_url.isnot(None)).count()}")

if __name__ == '__main__':
    create_sample_posts_with_images() 