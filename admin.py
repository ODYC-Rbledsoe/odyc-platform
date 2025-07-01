from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import User, Match, Session
from forms import MatchForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get statistics
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_mentors = User.query.filter_by(role='mentor').count()
    total_matches = Match.query.count()
    active_matches = Match.query.filter_by(status='active').count()
    total_sessions = Session.query.count()
    
    # Get recent activity
    recent_matches = Match.query.order_by(Match.created_at.desc()).limit(5).all()
    recent_sessions = Session.query.order_by(Session.created_at.desc()).limit(5).all()
    
    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_mentors': total_mentors,
        'total_matches': total_matches,
        'active_matches': active_matches,
        'total_sessions': total_sessions
    }
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         recent_matches=recent_matches,
                         recent_sessions=recent_sessions)

@admin_bp.route('/admin/create-match', methods=['GET', 'POST'])
@login_required
def create_match():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    form = MatchForm()
    
    # Get unmatched students and available mentors
    matched_student_ids = db.session.query(Match.student_id).filter_by(status='active').subquery()
    unmatched_students = User.query.filter(
        User.role == 'student',
        ~User.id.in_(matched_student_ids)
    ).all()
    
    available_mentors = User.query.filter_by(role='mentor').all()
    
    form.student_id.choices = [(s.id, f"{s.name} ({s.email})") for s in unmatched_students]
    form.mentor_id.choices = [(m.id, f"{m.name} ({m.email})") for m in available_mentors]
    
    if form.validate_on_submit():
        # Check if student is already matched
        existing_match = Match.query.filter_by(
            student_id=form.student_id.data,
            status='active'
        ).first()
        
        if existing_match:
            flash('Student is already matched with another mentor.', 'danger')
            return render_template('dashboard.html', form=form, action='Create Match')
        
        match = Match(
            student_id=form.student_id.data,
            mentor_id=form.mentor_id.data,
            status='active'
        )
        db.session.add(match)
        db.session.commit()
        
        student = User.query.get(form.student_id.data)
        mentor = User.query.get(form.mentor_id.data)
        flash(f'Match created successfully: {student.name} with {mentor.name}', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('dashboard.html', form=form, action='Create Match')

@admin_bp.route('/admin/manage-matches')
@login_required
def manage_matches():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    matches = Match.query.order_by(Match.created_at.desc()).all()
    return render_template('dashboard.html', matches=matches, action='Manage Matches')

@admin_bp.route('/admin/manage-users')
@login_required
def manage_users():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard.html', users=users, action='Manage Users')

@admin_bp.route('/admin/toggle-match-status/<int:match_id>')
@login_required
def toggle_match_status(match_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    match = Match.query.get_or_404(match_id)
    if match.status == 'active':
        match.status = 'completed'
        flash(f'Match between {match.student.name} and {match.mentor.name} marked as completed.', 'success')
    else:
        match.status = 'active'
        flash(f'Match between {match.student.name} and {match.mentor.name} reactivated.', 'success')
    
    db.session.commit()
    return redirect(url_for('admin.manage_matches'))

@admin_bp.route('/admin/delete-match/<int:match_id>')
@login_required
def delete_match(match_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    match = Match.query.get_or_404(match_id)
    student_name = match.student.name
    mentor_name = match.mentor.name
    
    db.session.delete(match)
    db.session.commit()
    
    flash(f'Match between {student_name} and {mentor_name} deleted successfully.', 'success')
    return redirect(url_for('admin.manage_matches'))
