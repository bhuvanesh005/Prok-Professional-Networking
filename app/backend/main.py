from flask import Flask
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager  # Add this import

# Load environment variables
load_dotenv()

# Import models and db
from models import db
from models.user import User
from models.profile import Profile, Skill, Experience, Education
from models.post import Post
from api.auth import auth_bp
from api.profile import profile_bp
from api.posts import posts_bp

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)
JWTManager(app)  # Initialize JWTManager here

def setup_database():
    """Setup database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(posts_bp)

# Create a function to initialize the app
def create_app():
    """Application factory function"""
    return app

if __name__ == '__main__':
    # Setup database tables
    setup_database()
    # Run the app
    app.run(debug=True)