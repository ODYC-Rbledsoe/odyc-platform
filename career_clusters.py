from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import CareerCluster, Industry, JobRole, CareerPathway, StudentCareerInterest

career_clusters_bp = Blueprint('career_clusters', __name__)

@career_clusters_bp.route('/career-clusters')
def explore_clusters():
    """Career clusters exploration page for all users"""
    # Get all clusters with priority ones first
    priority_clusters = CareerCluster.query.filter_by(is_priority_local=True).all()
    other_clusters = CareerCluster.query.filter_by(is_priority_local=False).all()
    
    return render_template('career_clusters/explore.html', 
                         priority_clusters=priority_clusters,
                         other_clusters=other_clusters)

@career_clusters_bp.route('/career-clusters/<int:cluster_id>')
def cluster_detail(cluster_id):
    """Detailed view of a specific career cluster"""
    cluster = CareerCluster.query.get_or_404(cluster_id)
    
    # Get local industries in this cluster
    local_industries = Industry.query.filter_by(career_cluster_id=cluster_id, is_active=True).all()
    
    # Get job roles in these industries
    industry_ids = [industry.id for industry in local_industries]
    job_roles = []
    if industry_ids:
        job_roles = JobRole.query.filter(JobRole.industry_id.in_(industry_ids)).all()
    
    # Get career pathways for these job roles
    job_role_ids = [role.id for role in job_roles]
    pathways = []
    if job_role_ids:
        pathways = CareerPathway.query.filter(CareerPathway.job_role_id.in_(job_role_ids), 
                                            CareerPathway.is_active == True).all()
    
    # Check if current user has interest in any pathways in this cluster
    user_interests = []
    if current_user.is_authenticated and current_user.is_student():
        pathway_ids = [pathway.id for pathway in pathways]
        if pathway_ids:
            user_interests = StudentCareerInterest.query.filter(
                StudentCareerInterest.student_id == current_user.id,
                StudentCareerInterest.pathway_id.in_(pathway_ids)
            ).all()
    
    return render_template('career_clusters/detail.html',
                         cluster=cluster,
                         local_industries=local_industries,
                         job_roles=job_roles,
                         pathways=pathways,
                         user_interests=user_interests)

@career_clusters_bp.route('/career-clusters/<int:cluster_id>/express-interest/<int:pathway_id>')
@login_required
def express_interest(cluster_id, pathway_id):
    """Allow students to express interest in a career pathway"""
    if not current_user.is_student():
        flash('Only students can express career interests.', 'warning')
        return redirect(url_for('career_clusters.cluster_detail', cluster_id=cluster_id))
    
    pathway = CareerPathway.query.get_or_404(pathway_id)
    
    # Check if interest already exists
    existing_interest = StudentCareerInterest.query.filter_by(
        student_id=current_user.id,
        pathway_id=pathway_id
    ).first()
    
    if existing_interest:
        flash(f'You have already expressed interest in {pathway.name}.', 'info')
    else:
        # Create new interest
        interest = StudentCareerInterest(
            student_id=current_user.id,
            pathway_id=pathway_id,
            interest_level='interested'
        )
        db.session.add(interest)
        db.session.commit()
        flash(f'Great! You have expressed interest in {pathway.name}. Your mentor will be notified.', 'success')
    
    return redirect(url_for('career_clusters.cluster_detail', cluster_id=cluster_id))

@career_clusters_bp.route('/my-career-interests')
@login_required
def my_interests():
    """View student's career interests and progress"""
    if not current_user.is_student():
        flash('Only students can view career interests.', 'warning')
        return redirect(url_for('dashboard.dashboard'))
    
    interests = StudentCareerInterest.query.filter_by(student_id=current_user.id).all()
    
    # Organize interests by cluster
    interests_by_cluster = {}
    for interest in interests:
        cluster = interest.pathway.job_role.industry.career_cluster
        if cluster.name not in interests_by_cluster:
            interests_by_cluster[cluster.name] = {
                'cluster': cluster,
                'interests': []
            }
        interests_by_cluster[cluster.name]['interests'].append(interest)
    
    return render_template('career_clusters/my_interests.html',
                         interests_by_cluster=interests_by_cluster)