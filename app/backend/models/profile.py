from models import db

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bio = db.Column(db.String(256))
    location = db.Column(db.String(128))
    phone = db.Column(db.String(32))  # Added phone field
    title = db.Column(db.String(128))  # Added title field
    languages = db.Column(db.String(256))  # New field
    connections = db.Column(db.Integer, default=0)  # New field
    mutualConnections = db.Column(db.Integer, default=0)  # New field
    # Add more fields as needed

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)

class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    company = db.Column(db.String(128))
    title = db.Column(db.String(128))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    school = db.Column(db.String(128))
    degree = db.Column(db.String(128))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    type = db.Column(db.String(64))
    content = db.Column(db.String(256))
    date = db.Column(db.String(32))
