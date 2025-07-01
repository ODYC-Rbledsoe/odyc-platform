from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import User, Match, Session
from forms import SessionForm, ProfileForm
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.admin_dashboard'))
    elif current_user.is_student():
        return render_template('student_dashboard.html')
    elif current_user.is_mentor():
        return render_template('mentor_dashboard.html')
    else:
        flash('Invalid user role.', 'danger')
        return redirect(url_for('auth.logout'))

@dashboard_bp.route('/student-dashboard')
@login_required
def student_dashboard():
    if not current_user.is_student():
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get student's match
    match = current_user.student_matches.filter_by(status='active').first()
    sessions = []
    if match:
        sessions = match.sessions.order_by(Session.date.desc()).all()
    
    return render_template('student_dashboard.html', match=match, sessions=sessions)

@dashboard_bp.route('/mentor-dashboard')
@login_required
def mentor_dashboard():
    if not current_user.is_mentor():
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get mentor's matches and sessions
    matches = current_user.mentor_matches.filter_by(status='active').all()
    return render_template('mentor_dashboard.html', matches=matches)

@dashboard_bp.route('/log-session/<int:match_id>', methods=['GET', 'POST'])
@login_required
def log_session(match_id):
    if not current_user.is_mentor():
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    match = Match.query.get_or_404(match_id)
    if match.mentor_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.mentor_dashboard'))
    
    form = SessionForm()
    if form.validate_on_submit():
        session = Session(
            match_id=match.id,
            date=form.date.data,
            topic=form.topic.data,
            notes=form.notes.data,
            student_reflection=form.student_reflection.data
        )
        db.session.add(session)
        db.session.commit()
        flash('Session logged successfully!', 'success')
        return redirect(url_for('dashboard.mentor_dashboard'))
    
    return render_template('dashboard.html', form=form, match=match, action='Log Session')

@dashboard_bp.route('/view-sessions/<int:match_id>')
@login_required
def view_sessions(match_id):
    match = Match.query.get_or_404(match_id)
    
    # Check if user has access to this match
    if not (current_user.is_admin() or 
            current_user.id == match.student_id or 
            current_user.id == match.mentor_id):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    sessions = match.sessions.order_by(Session.date.desc()).all()
    return render_template('dashboard.html', match=match, sessions=sessions, action='View Sessions')

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.interests_expertise = form.interests_expertise.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.bio.data = current_user.bio
        form.interests_expertise.data = current_user.interests_expertise
    
    return render_template('profile.html', form=form)

@dashboard_bp.route('/edit-session/<int:session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    session = Session.query.get_or_404(session_id)
    
    # Check if user has access to edit this session
    if not (current_user.is_admin() or current_user.id == session.match.mentor_id):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    form = SessionForm()
    if form.validate_on_submit():
        session.date = form.date.data
        session.topic = form.topic.data
        session.notes = form.notes.data
        session.student_reflection = form.student_reflection.data
        db.session.commit()
        flash('Session updated successfully!', 'success')
        return redirect(url_for('dashboard.view_sessions', match_id=session.match_id))
    elif request.method == 'GET':
        form.date.data = session.date
        form.topic.data = session.topic
        form.notes.data = session.notes
        form.student_reflection.data = session.student_reflection
    
    return render_template('dashboard.html', form=form, session=session, action='Edit Session')

@dashboard_bp.route('/delete-session/<int:session_id>', methods=['POST'])
@login_required
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    
    # Check if user has access to delete this session
    if not (current_user.is_admin() or current_user.id == session.match.mentor_id):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    match_id = session.match_id
    db.session.delete(session)
    db.session.commit()
    flash('Session deleted successfully!', 'success')
    return redirect(url_for('dashboard.view_sessions', match_id=match_id))
