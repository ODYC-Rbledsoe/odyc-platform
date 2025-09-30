"""Path Mapper - Job to Education Pathway Matching"""
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import JobPosting, EducationProgram, SkillAlignment, StudentPlan
from datetime import datetime, timedelta

path_mapper_bp = Blueprint('path_mapper', __name__, url_prefix='/path-mapper')

@path_mapper_bp.route('/')
@login_required
def index():
    """Landing page - choose or paste a job"""
    # Get available jobs
    jobs = JobPosting.query.filter_by(is_active=True).all()
    return render_template('path_mapper/job_picker.html', jobs=jobs)

@path_mapper_bp.route('/job/<int:job_id>/match')
@login_required
def program_match(job_id):
    """Show program match for selected job"""
    job = JobPosting.query.get_or_404(job_id)
    
    # Get all alignments for this job
    alignments = SkillAlignment.query.filter_by(job_id=job_id).all()
    
    # Group alignments by program
    programs_data = {}
    for alignment in alignments:
        program = alignment.program
        if program.id not in programs_data:
            programs_data[program.id] = {
                'program': program,
                'alignments': [],
                'covered_count': 0,
                'partial_count': 0,
                'missing_count': 0
            }
        
        programs_data[program.id]['alignments'].append(alignment)
        if alignment.coverage_level == 'covered':
            programs_data[program.id]['covered_count'] += 1
        elif alignment.coverage_level == 'partial':
            programs_data[program.id]['partial_count'] += 1
        else:
            programs_data[program.id]['missing_count'] += 1
    
    # Calculate coverage percentage for each program
    for program_data in programs_data.values():
        total_skills = len(job.skills_list)
        if total_skills > 0:
            program_data['coverage_pct'] = int(
                (program_data['covered_count'] / total_skills) * 100
            )
        else:
            program_data['coverage_pct'] = 0
    
    return render_template('path_mapper/program_match.html',
                          job=job,
                          programs_data=programs_data)

@path_mapper_bp.route('/job/<int:job_id>/program/<int:program_id>/plan', methods=['GET', 'POST'])
@login_required
def create_plan(job_id, program_id):
    """Create personalized enrollment plan"""
    job = JobPosting.query.get_or_404(job_id)
    program = EducationProgram.query.get_or_404(program_id)
    
    # Check if student already has a plan for this job/program
    existing_plan = StudentPlan.query.filter_by(
        student_id=current_user.id,
        job_id=job_id,
        program_id=program_id,
        status='active'
    ).first()
    
    if request.method == 'POST':
        # Create or update plan
        if existing_plan:
            plan = existing_plan
        else:
            # Default 4-step plan
            steps = [
                {
                    "step": "1. Apply to WWCC",
                    "description": "Complete online application for Industrial Maintenance Technology program",
                    "link": program.application_url,
                    "due_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                    "completed": False
                },
                {
                    "step": "2. Schedule Advising Appointment",
                    "description": "Meet with academic advisor to select courses for fastest certificate path",
                    "link": program.advising_url,
                    "due_date": (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
                    "completed": False
                },
                {
                    "step": "3. Complete Financial Aid",
                    "description": "Submit FAFSA and explore scholarship opportunities",
                    "link": program.financial_aid_url,
                    "due_date": (datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d'),
                    "completed": False
                },
                {
                    "step": "4. Prepare for Aptitude Test",
                    "description": "Review mechanical aptitude test materials (required by Simplot before interview)",
                    "link": None,
                    "due_date": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                    "completed": False
                }
            ]
            
            plan = StudentPlan(
                student_id=current_user.id,
                job_id=job_id,
                program_id=program_id,
                steps=json.dumps(steps),
                status='active',
                target_start_date=datetime.now() + timedelta(days=60),
                progress_pct=0
            )
            db.session.add(plan)
        
        db.session.commit()
        flash('Your pathway plan has been created!', 'success')
        return redirect(url_for('path_mapper.view_plan', plan_id=plan.id))
    
    return render_template('path_mapper/create_plan.html',
                          job=job,
                          program=program,
                          existing_plan=existing_plan)

@path_mapper_bp.route('/plan/<int:plan_id>')
@login_required
def view_plan(plan_id):
    """View student's personalized plan"""
    plan = StudentPlan.query.get_or_404(plan_id)
    
    # Security check
    if plan.student_id != current_user.id and not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('path_mapper.index'))
    
    # Get skill alignments for context
    alignments = SkillAlignment.query.filter_by(
        job_id=plan.job_id,
        program_id=plan.program_id
    ).all()
    
    coverage_pct = 0
    if plan.job.skills_list:
        covered = sum(1 for a in alignments if a.coverage_level == 'covered')
        coverage_pct = int((covered / len(plan.job.skills_list)) * 100)
    
    return render_template('path_mapper/view_plan.html',
                          plan=plan,
                          alignments=alignments,
                          coverage_pct=coverage_pct)

@path_mapper_bp.route('/plan/<int:plan_id>/update', methods=['POST'])
@login_required
def update_plan(plan_id):
    """Update plan step completion"""
    plan = StudentPlan.query.get_or_404(plan_id)
    
    # Security check
    if plan.student_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('path_mapper.index'))
    
    # Update steps
    steps = plan.steps_list
    step_index = int(request.form.get('step_index', 0))
    if 0 <= step_index < len(steps):
        steps[step_index]['completed'] = request.form.get('completed') == 'true'
        plan.steps = json.dumps(steps)
        
        # Update progress percentage
        completed_count = sum(1 for step in steps if step.get('completed'))
        plan.progress_pct = int((completed_count / len(steps)) * 100)
        
        db.session.commit()
        flash('Plan updated!', 'success')
    
    return redirect(url_for('path_mapper.view_plan', plan_id=plan_id))

@path_mapper_bp.route('/my-plans')
@login_required
def my_plans():
    """View all student's plans"""
    plans = StudentPlan.query.filter_by(student_id=current_user.id).order_by(StudentPlan.created_at.desc()).all()
    return render_template('path_mapper/my_plans.html', plans=plans)
