from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import (User, CurriculumModule, GroupProgress, StudentProgress, 
                   MentorGroup, GroupMembership)
from forms import (CurriculumModuleForm, AssignmentSubmissionForm, 
                   GradingForm, GroupProgressForm)
from datetime import datetime

curriculum_bp = Blueprint('curriculum', __name__)

# Admin routes for curriculum management
@curriculum_bp.route('/admin/curriculum')
@login_required
def manage_curriculum():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    modules = CurriculumModule.query.order_by(CurriculumModule.order_index).all()
    return render_template('curriculum/manage_curriculum.html', modules=modules)

@curriculum_bp.route('/admin/curriculum/create', methods=['GET', 'POST'])
@login_required
def create_module():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    form = CurriculumModuleForm()
    
    if form.validate_on_submit():
        module = CurriculumModule(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            learning_objectives=form.learning_objectives.data,
            resources=form.resources.data,
            assignments=form.assignments.data,
            duration_weeks=form.duration_weeks.data,
            difficulty_level=form.difficulty_level.data,
            order_index=form.order_index.data
        )
        
        db.session.add(module)
        db.session.commit()
        
        flash(f'Curriculum module "{module.title}" created successfully!', 'success')
        return redirect(url_for('curriculum.manage_curriculum'))
    
    return render_template('curriculum/create_module.html', form=form)

@curriculum_bp.route('/admin/curriculum/edit/<int:module_id>', methods=['GET', 'POST'])
@login_required
def edit_module(module_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    module = CurriculumModule.query.get_or_404(module_id)
    form = CurriculumModuleForm(obj=module)
    
    if form.validate_on_submit():
        form.populate_obj(module)
        module.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Module "{module.title}" updated successfully!', 'success')
        return redirect(url_for('curriculum.manage_curriculum'))
    
    return render_template('curriculum/edit_module.html', form=form, module=module)

# Mentor routes for curriculum delivery
@curriculum_bp.route('/mentor/curriculum')
@login_required
def mentor_curriculum():
    if not current_user.is_mentor():
        flash('Access denied. Mentor privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get mentor's groups
    groups = MentorGroup.query.filter_by(mentor_id=current_user.id, status='active').all()
    modules = CurriculumModule.query.filter_by(is_active=True).order_by(CurriculumModule.order_index).all()
    
    # Get progress for each group
    group_progress = {}
    for group in groups:
        progress = GroupProgress.query.filter_by(group_id=group.id).all()
        group_progress[group.id] = {p.module_id: p for p in progress}
    
    return render_template('curriculum/mentor_curriculum.html', 
                         groups=groups, modules=modules, group_progress=group_progress)

@curriculum_bp.route('/mentor/curriculum/module/<int:module_id>/group/<int:group_id>')
@login_required
def view_module_for_group(module_id, group_id):
    if not current_user.is_mentor():
        flash('Access denied. Mentor privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    group = MentorGroup.query.get_or_404(group_id)
    
    # Verify mentor owns this group
    if group.mentor_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('curriculum.mentor_curriculum'))
    
    module = CurriculumModule.query.get_or_404(module_id)
    
    # Get or create group progress
    group_progress = GroupProgress.query.filter_by(
        group_id=group_id, module_id=module_id
    ).first()
    
    if not group_progress:
        group_progress = GroupProgress(
            group_id=group_id,
            module_id=module_id,
            status='not_started'
        )
        db.session.add(group_progress)
        db.session.commit()
    
    # Get student progress for this module
    student_progress = StudentProgress.query.filter_by(
        module_id=module_id, group_id=group_id
    ).all()
    
    students = group.students
    
    return render_template('curriculum/module_detail.html', 
                         module=module, group=group, group_progress=group_progress,
                         student_progress=student_progress, students=students)

@curriculum_bp.route('/mentor/update-group-progress/<int:progress_id>', methods=['POST'])
@login_required
def update_group_progress(progress_id):
    if not current_user.is_mentor():
        flash('Access denied. Mentor privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    progress = GroupProgress.query.get_or_404(progress_id)
    
    # Verify mentor owns this group
    if progress.group.mentor_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('curriculum.mentor_curriculum'))
    
    form = GroupProgressForm()
    
    if form.validate_on_submit():
        progress.status = form.status.data
        progress.mentor_notes = form.mentor_notes.data
        
        if form.status.data == 'in_progress' and not progress.started_date:
            progress.started_date = datetime.utcnow()
        elif form.status.data == 'completed' and not progress.completed_date:
            progress.completed_date = datetime.utcnow()
        
        db.session.commit()
        flash('Group progress updated successfully!', 'success')
    
    return redirect(url_for('curriculum.view_module_for_group', 
                           module_id=progress.module_id, group_id=progress.group_id))

# Student routes for curriculum access
@curriculum_bp.route('/student/curriculum')
@login_required
def student_curriculum():
    if not current_user.is_student():
        flash('Access denied. Student privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get student's group membership
    membership = GroupMembership.query.filter_by(
        student_id=current_user.id, status='active'
    ).first()
    
    if not membership:
        flash('You are not currently assigned to a mentor group.', 'info')
        return render_template('curriculum/no_group.html')
    
    group = membership.group
    modules = CurriculumModule.query.filter_by(is_active=True).order_by(CurriculumModule.order_index).all()
    
    # Get student's progress
    student_progress = StudentProgress.query.filter_by(
        student_id=current_user.id, group_id=group.id
    ).all()
    progress_dict = {p.module_id: p for p in student_progress}
    
    # Get group progress
    group_progress = GroupProgress.query.filter_by(group_id=group.id).all()
    group_progress_dict = {p.module_id: p for p in group_progress}
    
    return render_template('curriculum/student_curriculum.html',
                         group=group, modules=modules, 
                         student_progress=progress_dict,
                         group_progress=group_progress_dict)

@curriculum_bp.route('/student/module/<int:module_id>')
@login_required
def student_view_module(module_id):
    if not current_user.is_student():
        flash('Access denied. Student privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get student's group membership
    membership = GroupMembership.query.filter_by(
        student_id=current_user.id, status='active'
    ).first()
    
    if not membership:
        flash('You are not currently assigned to a mentor group.', 'info')
        return redirect(url_for('curriculum.student_curriculum'))
    
    module = CurriculumModule.query.get_or_404(module_id)
    
    # Get or create student progress
    progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        module_id=module_id,
        group_id=membership.group_id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=current_user.id,
            module_id=module_id,
            group_id=membership.group_id,
            status='not_started'
        )
        db.session.add(progress)
        db.session.commit()
    
    return render_template('curriculum/student_module_view.html',
                         module=module, progress=progress, group=membership.group)

@curriculum_bp.route('/student/submit-assignment/<int:progress_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(progress_id):
    if not current_user.is_student():
        flash('Access denied. Student privileges required.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    progress = StudentProgress.query.get_or_404(progress_id)
    
    # Verify this is the student's progress
    if progress.student_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('curriculum.student_curriculum'))
    
    form = AssignmentSubmissionForm()
    
    if form.validate_on_submit():
        progress.assignment_content = form.assignment_content.data
        progress.assignment_submitted = True
        progress.status = 'completed'
        progress.completion_percentage = 100
        
        if not progress.started_date:
            progress.started_date = datetime.utcnow()
        progress.completed_date = datetime.utcnow()
        
        db.session.commit()
        
        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('curriculum.student_view_module', module_id=progress.module_id))
    
    # Pre-populate form if assignment was already submitted
    if progress.assignment_submitted:
        form.assignment_content.data = progress.assignment_content
    
    return render_template('curriculum/submit_assignment.html',
                         form=form, progress=progress, module=progress.module)