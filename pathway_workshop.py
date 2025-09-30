from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import (CareerPathway, ProjectCard, Rubric, Artifact, SkillsBadge, 
                   StudentBadge, SkillsTranscript, User)
from forms import (ProjectCardForm, RubricForm, ArtifactSubmissionForm, 
                  MentorSignoffForm, SkillsBadgeForm)
from datetime import datetime
import json

workshop_bp = Blueprint('workshop', __name__)

@workshop_bp.route('/workshop')
@login_required
def dashboard():
    """Pathway workshop dashboard for employers and educators"""
    if not (current_user.is_admin() or current_user.is_employer() or current_user.role == 'coordinator'):
        flash('Access denied. Workshop tools are for employers, coordinators, and administrators.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get all pathways with their project cards
    pathways = CareerPathway.query.filter_by(is_active=True).all()
    
    # Statistics
    total_projects = ProjectCard.query.filter_by(is_active=True).count()
    published_projects = ProjectCard.query.filter_by(is_active=True, is_published=True).count()
    total_rubrics = Rubric.query.count()
    total_badges = SkillsBadge.query.count()
    
    return render_template('workshop/dashboard.html',
                          pathways=pathways,
                          total_projects=total_projects,
                          published_projects=published_projects,
                          total_rubrics=total_rubrics,
                          total_badges=total_badges)

@workshop_bp.route('/workshop/pathway/<int:pathway_id>')
@login_required
def pathway_detail(pathway_id):
    """View all project cards for a pathway"""
    if not (current_user.is_admin() or current_user.is_employer() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    pathway = CareerPathway.query.get_or_404(pathway_id)
    project_cards = ProjectCard.query.filter_by(pathway_id=pathway_id, is_active=True).all()
    rubrics = Rubric.query.filter_by(pathway_id=pathway_id).all()
    badges = SkillsBadge.query.filter_by(pathway_id=pathway_id).all()
    
    return render_template('workshop/pathway_detail.html',
                          pathway=pathway,
                          project_cards=project_cards,
                          rubrics=rubrics,
                          badges=badges)

@workshop_bp.route('/workshop/project/new/<int:pathway_id>', methods=['GET', 'POST'])
@login_required
def create_project(pathway_id):
    """Create a new project card"""
    if not (current_user.is_admin() or current_user.is_employer() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    pathway = CareerPathway.query.get_or_404(pathway_id)
    form = ProjectCardForm()
    form.pathway_id.choices = [(pathway.id, pathway.name)]
    form.pathway_id.data = pathway.id
    
    if form.validate_on_submit():
        # Convert text fields to JSON arrays
        prereqs_list = [p.strip() for p in (form.prerequisites.data or '').split('\n') if p.strip()]
        steps_list = [s.strip() for s in (form.steps.data or '').split('\n') if s.strip()]
        tools_list = [t.strip() for t in (form.tools_materials.data or '').split('\n') if t.strip()] if form.tools_materials.data else []
        
        project = ProjectCard(
            pathway_id=form.pathway_id.data,
            title=form.title.data,
            objective=form.objective.data,
            duration_hours=form.duration_hours.data,
            prerequisites=json.dumps(prereqs_list),
            steps=json.dumps(steps_list),
            safety_notes=form.safety_notes.data,
            tools_materials=json.dumps(tools_list),
            ppe_required=form.ppe_required.data,
            artifact_type=form.artifact_type.data,
            artifact_description=form.artifact_description.data,
            location_type=form.location_type.data,
            capacity_per_month=form.capacity_per_month.data,
            mentor_required=form.mentor_required.data,
            supervisor_signoff=form.supervisor_signoff.data,
            created_by_id=current_user.id,
            is_active=True,
            is_published=False  # Requires educator approval
        )
        db.session.add(project)
        db.session.commit()
        
        flash(f'Project card "{project.title}" created successfully! It needs educator approval before publishing.', 'success')
        return redirect(url_for('workshop.pathway_detail', pathway_id=pathway_id))
    
    return render_template('workshop/project_form.html', form=form, pathway=pathway, edit_mode=False)

@workshop_bp.route('/workshop/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit an existing project card"""
    if not (current_user.is_admin() or current_user.is_employer() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    project = ProjectCard.query.get_or_404(project_id)
    form = ProjectCardForm(obj=project)
    form.pathway_id.choices = [(p.id, p.name) for p in CareerPathway.query.filter_by(is_active=True).all()]
    
    if request.method == 'GET':
        # Populate form with existing data
        form.pathway_id.data = project.pathway_id
        form.prerequisites.data = '\n'.join(project.prerequisites_list)
        form.steps.data = '\n'.join(project.steps_list)
        if project.tools_materials:
            try:
                tools_list = json.loads(project.tools_materials)
                form.tools_materials.data = '\n'.join(tools_list)
            except:
                pass
    
    if form.validate_on_submit():
        # Update project
        prereqs_list = [p.strip() for p in (form.prerequisites.data or '').split('\n') if p.strip()]
        steps_list = [s.strip() for s in (form.steps.data or '').split('\n') if s.strip()]
        tools_list = [t.strip() for t in (form.tools_materials.data or '').split('\n') if t.strip()] if form.tools_materials.data else []
        
        project.pathway_id = form.pathway_id.data
        project.title = form.title.data
        project.objective = form.objective.data
        project.duration_hours = form.duration_hours.data
        project.prerequisites = json.dumps(prereqs_list)
        project.steps = json.dumps(steps_list)
        project.safety_notes = form.safety_notes.data
        project.tools_materials = json.dumps(tools_list)
        project.ppe_required = form.ppe_required.data
        project.artifact_type = form.artifact_type.data
        project.artifact_description = form.artifact_description.data
        project.location_type = form.location_type.data
        project.capacity_per_month = form.capacity_per_month.data
        project.mentor_required = form.mentor_required.data
        project.supervisor_signoff = form.supervisor_signoff.data
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'Project card "{project.title}" updated successfully!', 'success')
        return redirect(url_for('workshop.pathway_detail', pathway_id=project.pathway_id))
    
    return render_template('workshop/project_form.html', form=form, pathway=project.pathway, 
                          project=project, edit_mode=True)

@workshop_bp.route('/workshop/project/<int:project_id>/publish', methods=['POST'])
@login_required
def publish_project(project_id):
    """Publish a project card for students (educator approval)"""
    if not (current_user.is_admin() or current_user.role == 'coordinator'):
        flash('Only coordinators and administrators can publish projects.', 'danger')
        return redirect(url_for('workshop.dashboard'))
    
    project = ProjectCard.query.get_or_404(project_id)
    project.is_published = True
    project.approved_by_id = current_user.id
    db.session.commit()
    
    flash(f'Project card "{project.title}" is now published and available to students!', 'success')
    return redirect(url_for('workshop.pathway_detail', pathway_id=project.pathway_id))

@workshop_bp.route('/workshop/project/<int:project_id>/unpublish', methods=['POST'])
@login_required
def unpublish_project(project_id):
    """Unpublish a project card"""
    if not (current_user.is_admin() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('workshop.dashboard'))
    
    project = ProjectCard.query.get_or_404(project_id)
    project.is_published = False
    db.session.commit()
    
    flash(f'Project card "{project.title}" has been unpublished.', 'info')
    return redirect(url_for('workshop.pathway_detail', pathway_id=project.pathway_id))

@workshop_bp.route('/workshop/rubric/new/<int:pathway_id>', methods=['GET', 'POST'])
@login_required
def create_rubric(pathway_id):
    """Create a new assessment rubric"""
    if not (current_user.is_admin() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('workshop.dashboard'))
    
    pathway = CareerPathway.query.get_or_404(pathway_id)
    form = RubricForm()
    form.pathway_id.choices = [(pathway.id, pathway.name)]
    form.pathway_id.data = pathway.id
    
    # Get project cards for this pathway
    project_cards = ProjectCard.query.filter_by(pathway_id=pathway_id, is_active=True).all()
    form.project_card_id.choices = [(0, 'General (not specific to a project)')] + \
                                    [(p.id, p.title) for p in project_cards]
    
    if form.validate_on_submit():
        rubric = Rubric(
            pathway_id=form.pathway_id.data,
            project_card_id=form.project_card_id.data if form.project_card_id.data != 0 else None,
            competency=form.competency.data,
            novice_criteria=form.novice_criteria.data,
            developing_criteria=form.developing_criteria.data,
            proficient_criteria=form.proficient_criteria.data,
            weight=form.weight.data,
            is_required=form.is_required.data
        )
        db.session.add(rubric)
        db.session.commit()
        
        flash(f'Rubric for "{rubric.competency}" created successfully!', 'success')
        return redirect(url_for('workshop.pathway_detail', pathway_id=pathway_id))
    
    return render_template('workshop/rubric_form.html', form=form, pathway=pathway)

@workshop_bp.route('/workshop/badge/new/<int:pathway_id>', methods=['GET', 'POST'])
@login_required
def create_badge(pathway_id):
    """Create a new skills badge"""
    if not (current_user.is_admin() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('workshop.dashboard'))
    
    pathway = CareerPathway.query.get_or_404(pathway_id)
    form = SkillsBadgeForm()
    form.pathway_id.choices = [(0, 'General (not pathway-specific)')] + \
                               [(p.id, p.name) for p in CareerPathway.query.filter_by(is_active=True).all()]
    
    # Get project cards for this pathway
    project_cards = ProjectCard.query.filter_by(pathway_id=pathway_id, is_active=True).all()
    form.project_card_id.choices = [(0, 'General (not project-specific)')] + \
                                    [(p.id, p.title) for p in project_cards]
    
    if form.validate_on_submit():
        badge = SkillsBadge(
            name=form.name.data,
            description=form.description.data,
            icon_class=form.icon_class.data,
            color_code=form.color_code.data,
            pathway_id=form.pathway_id.data if form.pathway_id.data != 0 else None,
            project_card_id=form.project_card_id.data if form.project_card_id.data != 0 else None,
            required_artifacts=form.required_artifacts.data,
            industry_recognized=form.industry_recognized.data,
            stackable=form.stackable.data
        )
        db.session.add(badge)
        db.session.commit()
        
        flash(f'Badge "{badge.name}" created successfully!', 'success')
        return redirect(url_for('workshop.pathway_detail', pathway_id=pathway_id))
    
    return render_template('workshop/badge_form.html', form=form, pathway=pathway)

# Student Routes
@workshop_bp.route('/projects')
@login_required
def student_projects():
    """Browse published project cards (student view)"""
    if not current_user.is_student():
        flash('This page is for students only.', 'warning')
        return redirect(url_for('workshop.dashboard'))
    
    # Get all published projects
    projects = ProjectCard.query.filter_by(is_active=True, is_published=True).all()
    
    # Get student's submissions
    my_artifacts = Artifact.query.filter_by(student_id=current_user.id).all()
    submitted_project_ids = [a.project_card_id for a in my_artifacts]
    
    return render_template('workshop/student_projects.html',
                          projects=projects,
                          submitted_project_ids=submitted_project_ids)

@workshop_bp.route('/project/<int:project_id>/view')
@login_required
def view_project(project_id):
    """View detailed project card"""
    project = ProjectCard.query.get_or_404(project_id)
    
    # Check if published for students, or if employer/admin viewing
    if not project.is_published and not (current_user.is_admin() or current_user.is_employer() or current_user.role == 'coordinator'):
        flash('This project is not yet published.', 'warning')
        return redirect(url_for('workshop.student_projects'))
    
    # Get student's existing artifact if any
    existing_artifact = None
    if current_user.is_student():
        existing_artifact = Artifact.query.filter_by(
            student_id=current_user.id,
            project_card_id=project_id
        ).first()
    
    return render_template('workshop/project_view.html',
                          project=project,
                          existing_artifact=existing_artifact)

@workshop_bp.route('/project/<int:project_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_artifact(project_id):
    """Submit artifact for a project"""
    if not current_user.is_student():
        flash('Only students can submit artifacts.', 'danger')
        return redirect(url_for('workshop.dashboard'))
    
    project = ProjectCard.query.get_or_404(project_id)
    
    if not project.is_published:
        flash('This project is not yet available for submission.', 'warning')
        return redirect(url_for('workshop.student_projects'))
    
    # Check if already submitted
    existing = Artifact.query.filter_by(
        student_id=current_user.id,
        project_card_id=project_id
    ).first()
    
    if existing and existing.status == 'approved':
        flash('You have already completed this project!', 'info')
        return redirect(url_for('workshop.view_project', project_id=project_id))
    
    form = ArtifactSubmissionForm()
    form.project_card_id.data = project_id
    
    if form.validate_on_submit():
        if existing:
            # Update existing submission
            existing.submission_text = form.submission_text.data
            existing.checklist_data = form.checklist_data.data
            existing.status = 'submitted'
            existing.submitted_at = datetime.utcnow()
            artifact = existing
        else:
            # Create new submission
            artifact = Artifact(
                student_id=current_user.id,
                project_card_id=project_id,
                submission_text=form.submission_text.data,
                checklist_data=form.checklist_data.data,
                status='submitted',
                submitted_at=datetime.utcnow()
            )
            db.session.add(artifact)
        
        db.session.commit()
        flash('Your project artifact has been submitted successfully! A mentor will review it soon.', 'success')
        return redirect(url_for('workshop.my_artifacts'))
    
    return render_template('workshop/submit_artifact.html',
                          form=form,
                          project=project,
                          existing_artifact=existing)

@workshop_bp.route('/my-artifacts')
@login_required
def my_artifacts():
    """View student's own artifact submissions"""
    if not current_user.is_student():
        flash('This page is for students only.', 'warning')
        return redirect(url_for('workshop.dashboard'))
    
    artifacts = Artifact.query.filter_by(student_id=current_user.id)\
                              .order_by(Artifact.submitted_at.desc()).all()
    
    # Get earned badges
    badges = StudentBadge.query.filter_by(student_id=current_user.id)\
                               .order_by(StudentBadge.earned_at.desc()).all()
    
    # Calculate stats
    approved_count = sum(1 for a in artifacts if a.status == 'approved')
    total_hours = sum(a.project_card.duration_hours for a in artifacts if a.status == 'approved')
    
    return render_template('workshop/my_artifacts.html',
                          artifacts=artifacts,
                          badges=badges,
                          approved_count=approved_count,
                          total_hours=total_hours)

# Mentor Routes
@workshop_bp.route('/mentor/review')
@login_required
def mentor_review_dashboard():
    """Mentor dashboard for reviewing artifacts"""
    if not (current_user.is_mentor() or current_user.is_admin() or current_user.role == 'coordinator'):
        flash('Access denied. This page is for mentors and coordinators.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get artifacts needing review
    pending = Artifact.query.filter_by(status='submitted')\
                           .order_by(Artifact.submitted_at.desc()).all()
    
    # Get recently reviewed
    reviewed = Artifact.query.filter(Artifact.status.in_(['approved', 'needs_revision']))\
                            .order_by(Artifact.reviewed_at.desc()).limit(20).all()
    
    return render_template('workshop/mentor_review.html',
                          pending=pending,
                          reviewed=reviewed)

@workshop_bp.route('/mentor/artifact/<int:artifact_id>/review', methods=['GET', 'POST'])
@login_required
def review_artifact(artifact_id):
    """Review and sign off on student artifact"""
    if not (current_user.is_mentor() or current_user.is_admin() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    artifact = Artifact.query.get_or_404(artifact_id)
    form = MentorSignoffForm()
    form.artifact_id.data = artifact_id
    
    if form.validate_on_submit():
        artifact.performance_level = form.performance_level.data
        artifact.mentor_feedback = form.mentor_feedback.data
        artifact.status = form.status.data
        artifact.reviewed_at = datetime.utcnow()
        artifact.mentor_signoff_id = current_user.id
        
        # If approved, check if student earns a badge
        if artifact.status == 'approved':
            # Check for badges associated with this project
            badges = SkillsBadge.query.filter_by(project_card_id=artifact.project_card_id).all()
            for badge in badges:
                # Check if student already has this badge
                existing_badge = StudentBadge.query.filter_by(
                    student_id=artifact.student_id,
                    badge_id=badge.id
                ).first()
                
                if not existing_badge:
                    student_badge = StudentBadge(
                        student_id=artifact.student_id,
                        badge_id=badge.id,
                        artifact_id=artifact.id,
                        earned_at=datetime.utcnow(),
                        verified_by_id=current_user.id
                    )
                    db.session.add(student_badge)
        
        db.session.commit()
        
        if artifact.status == 'approved':
            flash(f'Artifact approved! {artifact.student.name} has earned the badge.', 'success')
        else:
            flash(f'Feedback sent to {artifact.student.name}.', 'info')
        
        return redirect(url_for('workshop.mentor_review_dashboard'))
    
    return render_template('workshop/review_artifact.html',
                          form=form,
                          artifact=artifact)

# Skills Transcript
@workshop_bp.route('/transcript/<int:student_id>')
@login_required
def skills_transcript(student_id):
    """Generate skills transcript for a student"""
    # Only allow students to view their own, or mentors/admins to view any
    if current_user.id != student_id and not (current_user.is_admin() or current_user.is_mentor() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    from models import User
    student = User.query.get_or_404(student_id)
    
    if not student.is_student():
        flash('Skills transcripts are only available for students.', 'warning')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get student's completed artifacts
    artifacts = Artifact.query.filter_by(student_id=student_id, status='approved')\
                              .order_by(Artifact.reviewed_at.desc()).all()
    
    # Get earned badges
    badges = StudentBadge.query.filter_by(student_id=student_id)\
                               .order_by(StudentBadge.earned_at.desc()).all()
    
    # Calculate totals
    total_hours = sum(a.project_card.duration_hours for a in artifacts)
    pathways = set(a.project_card.pathway for a in artifacts)
    
    return render_template('workshop/skills_transcript.html',
                          student=student,
                          artifacts=artifacts,
                          badges=badges,
                          total_hours=total_hours,
                          pathways=pathways)

@workshop_bp.route('/transcript/<int:student_id>/pdf')
@login_required
def download_transcript_pdf(student_id):
    """Download skills transcript as PDF"""
    from io import BytesIO
    from flask import make_response
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from datetime import datetime
    
    # Authorization check
    if current_user.id != student_id and not (current_user.is_admin() or current_user.is_mentor() or current_user.role == 'coordinator'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    from models import User
    student = User.query.get_or_404(student_id)
    
    # Get data
    artifacts = Artifact.query.filter_by(student_id=student_id, status='approved')\
                              .order_by(Artifact.reviewed_at.desc()).all()
    badges = StudentBadge.query.filter_by(student_id=student_id)\
                               .order_by(StudentBadge.earned_at.desc()).all()
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E7D32'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=6
    )
    
    # Header
    story.append(Paragraph("ODYC Skills Transcript", title_style))
    story.append(Paragraph("Southwest Wyoming Workforce Development", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Student Info
    story.append(Paragraph("Student Information", heading_style))
    student_data = [
        ['Student Name:', student.name],
        ['Email:', student.email],
        ['Generated:', datetime.utcnow().strftime('%B %d, %Y')]
    ]
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(student_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Stats
    total_hours = sum(a.project_card.duration_hours for a in artifacts)
    story.append(Paragraph("Summary", heading_style))
    summary_data = [
        ['Completed Projects:', str(len(artifacts))],
        ['Total Training Hours:', f'{total_hours} hours'],
        ['Badges Earned:', str(len(badges))]
    ]
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Earned Badges
    if badges:
        story.append(Paragraph("Earned Credentials", heading_style))
        badge_data = [['Badge Name', 'Earned Date', 'Industry Recognized']]
        for sb in badges:
            badge_data.append([
                sb.badge.name,
                sb.earned_at.strftime('%m/%d/%Y'),
                'Yes' if sb.badge.industry_recognized else 'No'
            ])
        badge_table = Table(badge_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFC107')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(badge_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Completed Projects
    story.append(Paragraph("Completed Projects", heading_style))
    project_data = [['Project Title', 'Pathway', 'Hours', 'Performance', 'Completed']]
    for artifact in artifacts:
        project_data.append([
            artifact.project_card.title[:40],
            artifact.project_card.pathway.name[:30],
            str(artifact.project_card.duration_hours),
            artifact.performance_level.title() if artifact.performance_level else 'N/A',
            artifact.reviewed_at.strftime('%m/%d/%Y') if artifact.reviewed_at else 'N/A'
        ])
    project_table = Table(project_data, colWidths=[2.2*inch, 1.8*inch, 0.6*inch, 1*inch, 1*inch])
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(project_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = "This transcript documents hands-on project completion and skills development through ODYC's industry-partnered workforce development program."
    story.append(Paragraph(footer_text, styles['Italic']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Return PDF
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=ODYC_Skills_Transcript_{student.name.replace(" ", "_")}.pdf'
    
    return response
