from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .profile import Profile, Skill, Experience, Education, Activity
from .post import Post
from .job import Job, JobApplication
from .message import Message, Conversation