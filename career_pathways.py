from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import (CareerPathway, JobRole, Industry, StudentCareerInterest, 
                   EmployerPartner, PathwayModule, GroupMembership)
from datetime import datetime, timedelta

career_bp = Blueprint('career', __name__)

@career_bp.route('/career-pathways')
@login_required
def explore_pathways():
    """Show all available career pathways"""
    pathways = CareerPathway.query.filter_by(is_active=True).all()
    industries = Industry.query.filter_by(is_active=True).all()
    
    # Get student's current interests if they're a student
    student_interests = []
    if current_user.is_student():
        student_interests = StudentCareerInterest.query.filter_by(
            student_id=current_user.id
        ).all()
    
    return render_template('career/explore_pathways.html', 
                         pathways=pathways, industries=industries,
                         student_interests=student_interests)

@career_bp.route('/career-pathway/<int:pathway_id>')
@login_required
def view_pathway(pathway_id):
    """View detailed information about a specific career pathway"""
    pathway = CareerPathway.query.get_or_404(pathway_id)
    
    # Get pathway modules in order
    pathway_modules = PathwayModule.query.filter_by(
        pathway_id=pathway_id
    ).order_by(PathwayModule.order_in_pathway).all()
    
    # Get employer partners for this industry
    employers = EmployerPartner.query.filter_by(
        industry_id=pathway.job_role.industry_id,
        is_active=True
    ).all()
    
    # Check if student has interest in this pathway
    student_interest = None
    if current_user.is_student():
        student_interest = StudentCareerInterest.query.filter_by(
            student_id=current_user.id,
            pathway_id=pathway_id
        ).first()
    
    return render_template('career/pathway_detail.html',
                         pathway=pathway, pathway_modules=pathway_modules,
                         employers=employers, student_interest=student_interest)

@career_bp.route('/express-interest/<int:pathway_id>', methods=['POST'])
@login_required
def express_interest(pathway_id):
    """Student expresses interest in a career pathway"""
    if not current_user.is_student():
        flash('Only students can express career pathway interest.', 'danger')
        return redirect(url_for('career.explore_pathways'))
    
    pathway = CareerPathway.query.get_or_404(pathway_id)
    
    # Check if already interested
    existing_interest = StudentCareerInterest.query.filter_by(
        student_id=current_user.id,
        pathway_id=pathway_id
    ).first()
    
    if existing_interest:
        flash(f'You are already exploring the {pathway.name}.', 'info')
    else:
        # Create new interest record
        interest = StudentCareerInterest(
            student_id=current_user.id,
            pathway_id=pathway_id,
            interest_level='interested',
            target_completion=datetime.utcnow() + timedelta(days=pathway.duration_months * 30)
        )
        
        db.session.add(interest)
        db.session.commit()
        
        flash(f'Great! You are now exploring the {pathway.name}. Your mentor will help guide your journey.', 'success')
    
    return redirect(url_for('career.view_pathway', pathway_id=pathway_id))

@career_bp.route('/my-pathway')
@login_required
def my_pathway():
    """Student's personalized career roadmap"""
    if not current_user.is_student():
        flash('This feature is for students only.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get student's group membership
    membership = GroupMembership.query.filter_by(
        student_id=current_user.id, status='active'
    ).first()
    
    # Get student's career interests
    interests = StudentCareerInterest.query.filter_by(
        student_id=current_user.id
    ).order_by(StudentCareerInterest.started_date).all()
    
    # Get primary pathway (most recent or committed)
    primary_pathway = None
    if interests:
        primary_pathway = next(
            (interest for interest in interests if interest.interest_level == 'committed'),
            interests[0]  # Default to first if none committed
        )
    
    return render_template('career/my_pathway.html',
                         membership=membership, interests=interests,
                         primary_pathway=primary_pathway)

@career_bp.route('/industry-overview')
@login_required
def industry_overview():
    """Overview of Southwest Wyoming industries and opportunities"""
    industries = Industry.query.filter_by(is_active=True).all()
    
    # Get priority job roles (high demand)
    priority_roles = JobRole.query.filter_by(is_priority=True).order_by(
        JobRole.local_demand.desc()
    ).all()
    
    # Get active employer partners
    employers = EmployerPartner.query.filter_by(is_active=True).all()
    
    return render_template('career/industry_overview.html',
                         industries=industries, priority_roles=priority_roles,
                         employers=employers)

@career_bp.route('/update-interest/<int:interest_id>', methods=['POST'])
@login_required
def update_interest(interest_id):
    """Update student's career pathway interest level"""
    if not current_user.is_student():
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    interest = StudentCareerInterest.query.get_or_404(interest_id)
    
    # Verify student owns this interest
    if interest.student_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('career.my_pathway'))
    
    interest_level = request.form.get('interest_level')
    progress = request.form.get('progress_percentage', type=int)
    
    if interest_level in ['interested', 'exploring', 'committed']:
        interest.interest_level = interest_level
    
    if progress is not None and 0 <= progress <= 100:
        interest.progress_percentage = progress
    
    db.session.commit()
    
    flash('Your pathway progress has been updated!', 'success')
    return redirect(url_for('career.my_pathway'))