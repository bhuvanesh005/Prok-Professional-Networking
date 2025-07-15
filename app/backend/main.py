from flask import Flask
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager  # Add this import

# Load environment variables
load_dotenv()

# Import models and db
from models import db
from api.auth import auth_bp
from api.profile import profile_bp
from api.posts import posts_bp
from api.feed import feed_bp
from api.messaging import messaging_bp
from api.jobs import jobs_bp

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app, origins=['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175'], supports_credentials=True)
db.init_app(app)
JWTManager(app)  # Initialize JWTManager here

def setup_database():
    """Setup database tables"""
    with app.app_context():
        # Import models after app context is created
        from models.user import User
        from models.profile import Profile, Skill, Experience, Education
        from models.post import Post
        from models.job import Job, JobApplication
        from models.message import Message, Conversation
        
        db.create_all()
        print("✅ Database tables created successfully!")

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(messaging_bp)
app.register_blueprint(jobs_bp)

# Create a function to initialize the app
def create_app():
    """Application factory function"""
    return app

if __name__ == '__main__':
    # Setup database tables
    setup_database()
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)