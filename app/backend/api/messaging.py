from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.message import Message, Conversation
from models.user import User
from models.profile import Profile
from models import db
from sqlalchemy import desc
from datetime import datetime

messaging_bp = Blueprint('messaging', __name__)

@messaging_bp.route('/api/messages/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for the current user"""
    try:
        user_id = get_jwt_identity()
        
        # Get conversations where user is either sender or receiver
        conversations = Conversation.query.filter(
            (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
        ).all()
        
        conversation_list = []
        for conv in conversations:
            # Determine the other user in the conversation
            other_user_id = conv.user2_id if conv.user1_id == user_id else conv.user1_id
            other_user = User.query.get(other_user_id)
            
            if other_user and other_user.profile:
                conversation_list.append({
                    'id': conv.id,
                    'other_user': {
                        'id': other_user.id,
                        'name': other_user.username,
                        'avatar_url': other_user.profile.avatar_url,
                        'title': other_user.profile.title
                    },
                    'last_message': conv.last_message,
                    'last_message_time': conv.last_message_time.isoformat() if conv.last_message_time else None,
                    'unread_count': conv.unread_count or 0
                })
        
        return jsonify({'conversations': conversation_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messaging_bp.route('/api/messages/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    """Get messages for a specific conversation"""
    try:
        user_id = get_jwt_identity()
        
        # Verify user is part of this conversation
        conversation = Conversation.query.filter(
            (Conversation.id == conversation_id) &
            ((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id))
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Get messages for this conversation
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
        
        message_list = []
        for msg in messages:
            sender = User.query.get(msg.sender_id)
            message_list.append({
                'id': msg.id,
                'content': msg.content,
                'sender_id': msg.sender_id,
                'sender_name': sender.username if sender else 'Unknown',
                'created_at': msg.created_at.isoformat() if msg.created_at else None,
                'is_own': msg.sender_id == user_id
            })
        
        return jsonify({'messages': message_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messaging_bp.route('/api/messages/<int:conversation_id>', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    """Send a message in a conversation"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({'error': 'Message content is required'}), 400
        
        # Verify user is part of this conversation
        conversation = Conversation.query.filter(
            (Conversation.id == conversation_id) &
            ((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id))
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Create new message
        new_message = Message(
            conversation_id=conversation_id,
            sender_id=user_id,
            content=content,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_message)
        
        # Update conversation with last message info
        conversation.last_message = content
        conversation.last_message_time = datetime.utcnow()
        conversation.unread_count = (conversation.unread_count or 0) + 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent successfully',
            'message_id': new_message.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 