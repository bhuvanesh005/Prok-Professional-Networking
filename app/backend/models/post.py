from . import db
from sqlalchemy.sql import func
from sqlalchemy import Index

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(100), nullable=True, default='general')
    tags = db.Column(db.Text, nullable=True)  # JSON string of tags
    visibility = db.Column(db.String(20), nullable=False, default='public')  # public, private, connections
    likes_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    # Add indexes for better query performance
    __table_args__ = (
        Index('idx_post_created_at', 'created_at'),
        Index('idx_post_category', 'category'),
        Index('idx_post_visibility', 'visibility'),
        Index('idx_post_likes_count', 'likes_count'),
        Index('idx_post_views_count', 'views_count'),
        Index('idx_post_user_id', 'user_id'),
    )

    def to_dict(self):
        import json
        tags_list = []
        if self.tags:
            try:
                tags_list = json.loads(self.tags)
            except:
                tags_list = []
        
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'media_url': self.media_url,
            'user_id': self.user_id,
            'category': self.category,
            'tags': tags_list,
            'visibility': self.visibility,
            'likes_count': self.likes_count,
            'views_count': self.views_count,
            'comments_count': self.comments_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': self.user.username if self.user else None
        }
