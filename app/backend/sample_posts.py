# sample_posts.py
"""
Script to create sample posts for testing the posts listing functionality.
Run this after setting up the database to populate it with test data.
"""
import json
from models import db
from models.post import Post
from models.user import User
from main import app

def create_sample_posts():
    """Create sample posts with various categories, tags, and content"""
    
    with app.app_context():
        # Get the first user (or create one if none exists)
        user = User.query.first()
        if not user:
            print("No users found. Please create a user first.")
            return
        
        # Sample posts data
        sample_posts = [
            {
                'title': 'Getting Started with React Development',
                'content': '<p>React is a powerful JavaScript library for building user interfaces. In this post, I\'ll share some tips for getting started with React development.</p><p>Key points to remember:</p><ul><li>Components are the building blocks</li><li>Props are for passing data down</li><li>State is for managing component data</li></ul>',
                'category': 'technology',
                'tags': ['react', 'javascript', 'frontend', 'web-development'],
                'visibility': 'public',
                'likes_count': 15,
                'views_count': 120
            },
            {
                'title': 'Python Best Practices for Backend Development',
                'content': '<p>Python is an excellent choice for backend development. Here are some best practices I\'ve learned over the years.</p><p>Focus on:</p><ul><li>Code readability</li><li>Error handling</li><li>Performance optimization</li><li>Security best practices</li></ul>',
                'category': 'programming',
                'tags': ['python', 'backend', 'best-practices', 'api'],
                'visibility': 'public',
                'likes_count': 23,
                'views_count': 89
            },
            {
                'title': 'Career Tips for Software Engineers',
                'content': '<p>Building a successful career in software engineering requires more than just technical skills. Here are some insights from my experience.</p><p>Important aspects:</p><ul><li>Continuous learning</li><li>Networking</li><li>Soft skills development</li><li>Work-life balance</li></ul>',
                'category': 'career',
                'tags': ['career', 'software-engineering', 'professional-development'],
                'visibility': 'public',
                'likes_count': 8,
                'views_count': 45
            },
            {
                'title': 'Machine Learning Fundamentals',
                'content': '<p>Machine learning is transforming industries across the globe. Let\'s explore the fundamental concepts.</p><p>Core concepts:</p><ul><li>Supervised vs Unsupervised Learning</li><li>Feature Engineering</li><li>Model Evaluation</li><li>Overfitting Prevention</li></ul>',
                'category': 'ai-ml',
                'tags': ['machine-learning', 'ai', 'data-science', 'algorithms'],
                'visibility': 'public',
                'likes_count': 31,
                'views_count': 156
            },
            {
                'title': 'Web Security Best Practices',
                'content': '<p>Security should be a top priority in web development. Here are essential practices to protect your applications.</p><p>Key areas:</p><ul><li>Input validation</li><li>Authentication & Authorization</li><li>Data encryption</li><li>Regular security audits</li></ul>',
                'category': 'security',
                'tags': ['security', 'web-development', 'authentication', 'encryption'],
                'visibility': 'public',
                'likes_count': 19,
                'views_count': 78
            },
            {
                'title': 'Database Design Principles',
                'content': '<p>Good database design is crucial for application performance and maintainability. Let\'s discuss key principles.</p><p>Design principles:</p><ul><li>Normalization</li><li>Indexing strategies</li><li>Relationship modeling</li><li>Performance optimization</li></ul>',
                'category': 'database',
                'tags': ['database', 'sql', 'design', 'performance'],
                'visibility': 'public',
                'likes_count': 12,
                'views_count': 67
            },
            {
                'title': 'DevOps and CI/CD Pipeline',
                'content': '<p>DevOps practices and CI/CD pipelines are essential for modern software development. Here\'s what you need to know.</p><p>Pipeline components:</p><ul><li>Automated testing</li><li>Build automation</li><li>Deployment strategies</li><li>Monitoring and logging</li></ul>',
                'category': 'devops',
                'tags': ['devops', 'ci-cd', 'automation', 'deployment'],
                'visibility': 'public',
                'likes_count': 27,
                'views_count': 134
            },
            {
                'title': 'Mobile App Development Trends',
                'content': '<p>The mobile app development landscape is constantly evolving. Let\'s explore current trends and technologies.</p><p>Trending technologies:</p><ul><li>Cross-platform frameworks</li><li>Progressive Web Apps</li><li>AI integration</li><li>5G optimization</li></ul>',
                'category': 'mobile',
                'tags': ['mobile-development', 'react-native', 'flutter', 'pwa'],
                'visibility': 'public',
                'likes_count': 14,
                'views_count': 92
            },
            {
                'title': 'Cloud Computing Services Overview',
                'content': '<p>Cloud computing has revolutionized how we build and deploy applications. Here\'s an overview of major services.</p><p>Service categories:</p><ul><li>Infrastructure as a Service (IaaS)</li><li>Platform as a Service (PaaS)</li><li>Software as a Service (SaaS)</li><li>Serverless computing</li></ul>',
                'category': 'cloud',
                'tags': ['cloud-computing', 'aws', 'azure', 'google-cloud'],
                'visibility': 'public',
                'likes_count': 21,
                'views_count': 103
            },
            {
                'title': 'Agile Development Methodology',
                'content': '<p>Agile methodology has become the standard for modern software development teams. Let\'s explore its principles and practices.</p><p>Agile principles:</p><ul><li>Sprint planning</li><li>Daily standups</li><li>Retrospectives</li><li>Continuous improvement</li></ul>',
                'category': 'methodology',
                'tags': ['agile', 'scrum', 'project-management', 'team-collaboration'],
                'visibility': 'public',
                'likes_count': 16,
                'views_count': 88
            }
        ]
        
        # Create posts
        created_count = 0
        for post_data in sample_posts:
            # Check if post already exists (by title)
            existing_post = Post.query.filter_by(title=post_data['title']).first()
            if not existing_post:
                post = Post(
                    title=post_data['title'],
                    content=post_data['content'],
                    category=post_data['category'],
                    tags=json.dumps(post_data['tags']),
                    visibility=post_data['visibility'],
                    likes_count=post_data['likes_count'],
                    views_count=post_data['views_count'],
                    user_id=user.id
                )
                db.session.add(post)
                created_count += 1
        
        db.session.commit()
        print(f"✅ Created {created_count} sample posts successfully!")
        print(f"📊 Total posts in database: {Post.query.count()}")

if __name__ == '__main__':
    create_sample_posts() 