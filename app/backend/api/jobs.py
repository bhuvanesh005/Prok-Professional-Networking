from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.job import Job, JobApplication
from models.user import User
from models.profile import Profile
from models import db
from sqlalchemy import desc
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/api/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get all available jobs"""
    try:
        # Get query parameters for filtering
        category = request.args.get('category')
        location = request.args.get('location')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = Job.query.filter_by(status='active')
        
        if category:
            query = query.filter(Job.category == category)
        if location:
            query = query.filter(Job.location.contains(location))
        
        # Get paginated results
        jobs = query.order_by(desc(Job.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        job_list = []
        for job in jobs.items:
            job_list.append({
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'category': job.category,
                'description': job.description,
                'requirements': job.requirements,
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'employment_type': job.employment_type,
                'experience_level': job.experience_level,
                'created_at': job.created_at.isoformat() if job.created_at else None,
                'posted_by': {
                    'id': job.posted_by,
                    'name': User.query.get(job.posted_by).username if User.query.get(job.posted_by) else 'Unknown'
                }
            })
        
        return jsonify({
            'jobs': job_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': jobs.total,
                'pages': jobs.pages,
                'has_next': jobs.has_next,
                'has_prev': jobs.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/api/jobs/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get a specific job by ID"""
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        job_data = {
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'category': job.category,
            'description': job.description,
            'requirements': job.requirements,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'employment_type': job.employment_type,
            'experience_level': job.experience_level,
            'created_at': job.created_at.isoformat() if job.created_at else None,
            'posted_by': {
                'id': job.posted_by,
                'name': User.query.get(job.posted_by).username if User.query.get(job.posted_by) else 'Unknown'
            }
        }
        
        return jsonify(job_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_job(job_id):
    """Apply for a job"""
    try:
        user_id = get_jwt_identity()
        
        # Check if job exists
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Check if job is active
        if job.status != 'active':
            return jsonify({'error': 'Job is not available for applications'}), 400
        
        # Check if user already applied
        existing_application = JobApplication.query.filter_by(
            job_id=job_id, 
            applicant_id=user_id
        ).first()
        
        if existing_application:
            return jsonify({'error': 'You have already applied for this job'}), 400
        
        # Create application
        application = JobApplication(
            job_id=job_id,
            applicant_id=user_id,
            status='pending',
            applied_at=datetime.utcnow()
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 