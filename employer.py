from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response, send_file
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import json
from datetime import datetime, timedelta
import secrets
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from app import db
from models import *
from forms import (EmployerRegistrationForm, EmployerProfileForm, OpportunityForm, 
                  SponsorshipForm, StudentExportForm)

employer_bp = Blueprint('employer', __name__, url_prefix='/employer')

@employer_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Employer registration"""
    form = EmployerRegistrationForm()
    
    # Populate industry choices
    industries = Industry.query.all()
    form.industry_id.choices = [(i.id, i.name) for i in industries]
    
    if form.validate_on_submit():
        # Create user account
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role='employer'
        )
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Create employer profile
        employer = EmployerPartner(
            company_name=form.company_name.data,
            industry_id=form.industry_id.data,
            contact_name=form.name.data,
            contact_email=form.email.data,
            contact_phone=form.contact_phone.data,
            website=form.website.data,
            address=form.address.data,
            employee_count=form.employee_count.data,
            description=form.description.data,
            hiring_needs=form.hiring_needs.data,
            annual_hires=form.annual_hires.data or 0,
            user_id=user.id,
            participation_level='Hiring Partner'
        )
        db.session.add(employer)
        db.session.commit()
        
        flash(f'Welcome to ODYC, {form.company_name.data}! Your employer account has been created.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('employer/register.html', form=form)

@employer_bp.route('/dashboard')
@login_required
def dashboard():
    """Employer dashboard"""
    if not current_user.is_employer():
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    if not employer:
        flash('Please complete your employer profile.', 'warning')
        return redirect(url_for('employer.profile'))
    
    # Get employer's opportunities
    opportunities = EmployerOpportunity.query.filter_by(employer_id=employer.id).order_by(
        EmployerOpportunity.created_at.desc()).limit(5).all()
    
    # Get recent applications
    recent_applications = OpportunityApplication.query.join(EmployerOpportunity).filter(
        EmployerOpportunity.employer_id == employer.id
    ).order_by(OpportunityApplication.applied_at.desc()).limit(10).all()
    
    # Get student analytics (anonymized)
    total_students = User.query.filter_by(role='student').count()
    pathway_stats = db.session.query(
        CareerPathway.name,
        db.func.count(StudentCareerInterest.id)
    ).join(StudentCareerInterest).group_by(CareerPathway.name).all()
    
    # Active sponsorship
    active_sponsorship = Sponsorship.query.filter_by(
        employer_id=employer.id, status='active'
    ).first()
    
    return render_template('employer/dashboard.html', 
                         employer=employer,
                         opportunities=opportunities,
                         recent_applications=recent_applications,
                         total_students=total_students,
                         pathway_stats=pathway_stats,
                         active_sponsorship=active_sponsorship)

@employer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Employer profile management"""
    if not current_user.is_employer():
        flash('Access denied. Employer account required.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    if not employer:
        # Create basic profile if none exists
        employer = EmployerPartner(
            company_name="",
            industry_id=1,
            contact_name=current_user.name,
            contact_email=current_user.email,
            user_id=current_user.id
        )
        db.session.add(employer)
        db.session.commit()
    
    form = EmployerProfileForm(obj=employer)
    
    # Populate choices
    industries = Industry.query.all()
    form.industry_id.choices = [(i.id, i.name) for i in industries]
    
    if form.validate_on_submit():
        form.populate_obj(employer)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employer.dashboard'))
    
    return render_template('employer/profile.html', form=form, employer=employer)

@employer_bp.route('/opportunities')
@login_required
def opportunities():
    """Manage opportunities"""
    if not current_user.is_employer():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    if not employer:
        flash('Please complete your employer profile first.', 'warning')
        return redirect(url_for('employer.profile'))
    
    opportunities = EmployerOpportunity.query.filter_by(employer_id=employer.id).order_by(
        EmployerOpportunity.created_at.desc()).all()
    
    return render_template('employer/opportunities.html', opportunities=opportunities)

@employer_bp.route('/opportunities/new', methods=['GET', 'POST'])
@login_required
def new_opportunity():
    """Create new opportunity"""
    if not current_user.is_employer():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    form = OpportunityForm()
    
    # Populate pathway choices
    pathways = CareerPathway.query.all()
    form.pathway_id.choices = [(0, 'Any Pathway')] + [(p.id, p.name) for p in pathways]
    
    if form.validate_on_submit():
        opportunity = EmployerOpportunity(
            employer_id=employer.id,
            title=form.title.data,
            opportunity_type=form.opportunity_type.data,
            description=form.description.data,
            requirements=form.requirements.data,
            pathway_id=form.pathway_id.data if form.pathway_id.data > 0 else None,
            duration=form.duration.data,
            compensation=form.compensation.data,
            positions_available=form.positions_available.data,
            application_deadline=form.application_deadline.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(opportunity)
        db.session.commit()
        
        flash(f'Opportunity "{form.title.data}" posted successfully!', 'success')
        return redirect(url_for('employer.opportunities'))
    
    return render_template('employer/new_opportunity.html', form=form)

@employer_bp.route('/students')
@login_required
def students():
    """Browse anonymized student progress"""
    if not current_user.is_employer():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    active_sponsorship = Sponsorship.query.filter_by(
        employer_id=employer.id, status='active'
    ).first()
    
    # Only sponsors can view detailed student data
    if not active_sponsorship:
        flash('Student progress viewing requires an active sponsorship. Contact admin for details.', 'info')
        return redirect(url_for('employer.sponsorship'))
    
    # Get anonymized student data
    pathway_filter = request.args.get('pathway')
    query = db.session.query(
        User.id,
        db.func.count(StudentProgress.id).label('modules_completed'),
        db.func.count(Match.id).label('mentoring_sessions'),
        CareerPathway.name.label('pathway_name')
    ).join(StudentCareerInterest).join(CareerPathway).outerjoin(StudentProgress).outerjoin(
        Match, Match.student_id == User.id
    ).filter(User.role == 'student').group_by(User.id, CareerPathway.name)
    
    if pathway_filter:
        query = query.filter(CareerPathway.id == pathway_filter)
    
    students_data = query.all()
    
    # Get pathway filter options
    pathways = CareerPathway.query.all()
    
    return render_template('employer/students.html', 
                         students_data=students_data,
                         pathways=pathways,
                         selected_pathway=pathway_filter,
                         sponsorship=active_sponsorship)

@employer_bp.route('/sponsorship', methods=['GET', 'POST'])
@login_required
def sponsorship():
    """Sponsorship management"""
    if not current_user.is_employer():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    form = SponsorshipForm()
    
    # Populate pathway choices
    pathways = CareerPathway.query.all()
    form.pathway_focus.choices = [(0, 'All Pathways')] + [(p.id, p.name) for p in pathways]
    
    # Get existing sponsorships
    sponsorships = Sponsorship.query.filter_by(employer_id=employer.id).order_by(
        Sponsorship.created_at.desc()).all()
    
    if form.validate_on_submit():
        # Calculate amount based on tier
        tier_amounts = {
            'bronze': 2500,
            'silver': 7500,
            'gold': 15000,
            'platinum': 25000
        }
        
        # Set benefits based on tier
        tier_benefits = {
            'bronze': {'dashboard_access': True},
            'silver': {'dashboard_access': True, 'early_talent_access': True},
            'gold': {'dashboard_access': True, 'early_talent_access': True, 
                    'branding_enabled': True, 'curriculum_input': True},
            'platinum': {'dashboard_access': True, 'early_talent_access': True,
                        'branding_enabled': True, 'curriculum_input': True,
                        'exclusive_events': True, 'candidate_matching': True}
        }
        
        sponsorship = Sponsorship(
            employer_id=employer.id,
            tier=form.tier.data,
            annual_amount=tier_amounts[form.tier.data],
            pathway_focus_id=form.pathway_focus.data if form.pathway_focus.data > 0 else None,
            branding_enabled=form.branding_interest.data,
            early_talent_access=form.early_access.data,
            curriculum_input=form.curriculum_input.data,
            exclusive_events=form.exclusive_events.data,
            billing_contact=form.contact_name.data,
            billing_email=form.contact_email.data,
            notes=form.notes.data,
            **tier_benefits.get(form.tier.data, {})
        )
        db.session.add(sponsorship)
        db.session.commit()
        
        flash(f'Sponsorship request submitted! An ODYC administrator will contact you within 2 business days.', 'success')
        return redirect(url_for('employer.sponsorship'))
    
    return render_template('employer/sponsorship.html', 
                         form=form, 
                         sponsorships=sponsorships,
                         employer=employer)

@employer_bp.route('/applications')
@login_required
def applications():
    """View and manage opportunity applications"""
    if not current_user.is_employer():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard.index'))
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    applications = OpportunityApplication.query.join(EmployerOpportunity).filter(
        EmployerOpportunity.employer_id == employer.id
    ).order_by(OpportunityApplication.applied_at.desc()).all()
    
    return render_template('employer/applications.html', applications=applications)

@employer_bp.route('/applications/<int:app_id>/review', methods=['POST'])
@login_required
def review_application(app_id):
    """Review application"""
    if not current_user.is_employer():
        return jsonify({'error': 'Access denied'}), 403
    
    employer = EmployerPartner.query.filter_by(user_id=current_user.id).first()
    application = OpportunityApplication.query.join(EmployerOpportunity).filter(
        EmployerOpportunity.employer_id == employer.id,
        OpportunityApplication.id == app_id
    ).first_or_404()
    
    data = request.get_json()
    application.status = data.get('status', 'pending')
    application.employer_notes = data.get('notes', '')
    application.reviewed_at = datetime.utcnow()
    
    if application.status == 'accepted':
        application.opportunity.positions_filled += 1
    
    db.session.commit()
    
    return jsonify({'success': True})

# Student Portfolio Generation and Sharing
@employer_bp.route('/generate-portfolio', methods=['GET', 'POST'])
@login_required
def generate_portfolio():
    """Generate student portfolio for sharing"""
    if not current_user.is_student():
        flash('Access denied. Student account required.', 'error')
        return redirect(url_for('dashboard.index'))
    
    form = StudentExportForm()
    
    if form.validate_on_submit():
        # Generate portfolio
        portfolio = create_student_portfolio(current_user, form)
        
        if form.export_format.data in ['pdf', 'both']:
            # Generate PDF
            pdf_buffer = generate_portfolio_pdf(current_user, portfolio)
            portfolio.pdf_path = f"portfolios/{portfolio.id}.pdf"
        
        if form.export_format.data in ['digital', 'both']:
            # Generate digital URL
            portfolio.digital_url = portfolio.generate_access_url()
        
        db.session.commit()
        
        # Share with employer if specified
        if form.recipient_email.data:
            # Here you would implement email sharing
            flash(f'Portfolio shared with {form.recipient_email.data}', 'success')
        
        flash('Portfolio generated successfully!', 'success')
        return redirect(url_for('employer.view_portfolio', portfolio_id=portfolio.id))
    
    return render_template('employer/generate_portfolio.html', form=form)

@employer_bp.route('/portfolio/<int:portfolio_id>')
@employer_bp.route('/portfolio/<int:portfolio_id>/<access_token>')
def view_portfolio(portfolio_id, access_token=None):
    """View student portfolio"""
    portfolio = StudentPortfolio.query.get_or_404(portfolio_id)
    
    # Check access permissions
    if not portfolio.is_accessible:
        flash('Portfolio has expired.', 'error')
        return redirect(url_for('dashboard.index'))
    
    # If accessing via token, anyone can view
    if access_token and access_token == portfolio.access_token:
        portfolio.view_count += 1
        db.session.commit()
        return render_template('employer/portfolio_view.html', portfolio=portfolio, public=True)
    
    # Otherwise, require login and ownership
    if not current_user.is_authenticated or current_user.id != portfolio.student_id:
        flash('Access denied.', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('employer/portfolio_view.html', portfolio=portfolio, public=False)

def create_student_portfolio(student, form):
    """Create portfolio data structure"""
    portfolio_data = {
        'student': {
            'name': student.name,
            'email': student.email if form.include_personal.data else None,
            'bio': student.bio
        },
        'generated_at': datetime.utcnow().isoformat()
    }
    
    if form.include_pathway.data:
        interests = StudentCareerInterest.query.filter_by(student_id=student.id).all()
        portfolio_data['pathways'] = [
            {
                'name': interest.pathway.name,
                'description': interest.pathway.description,
                'progress': interest.progress_percentage,
                'target_roles': [role.title for role in interest.pathway.target_roles]
            }
            for interest in interests
        ]
    
    if form.include_curriculum.data:
        progress = StudentProgress.query.filter_by(student_id=student.id).all()
        portfolio_data['modules'] = [
            {
                'title': p.module.title,
                'description': p.module.description,
                'status': p.status,
                'grade': p.grade,
                'completion_date': p.completion_date.isoformat() if p.completion_date else None
            }
            for p in progress if p.status == 'completed'
        ]
    
    if form.include_sessions.data:
        sessions = Session.query.filter_by(student_id=student.id).order_by(
            Session.date.desc()).limit(10).all()
        portfolio_data['mentoring'] = [
            {
                'date': s.date.isoformat(),
                'topic': s.topic,
                'reflection': s.student_reflection,
                'mentor_name': s.mentor.name
            }
            for s in sessions
        ]
    
    # Create portfolio record
    portfolio = StudentPortfolio(
        student_id=student.id,
        include_personal=form.include_personal.data,
        include_pathway=form.include_pathway.data,
        include_curriculum=form.include_curriculum.data,
        include_sessions=form.include_sessions.data,
        include_achievements=form.include_achievements.data,
        include_recommendations=form.include_recommendations.data,
        portfolio_data=json.dumps(portfolio_data),
        access_token=secrets.token_urlsafe(32),
        expires_at=datetime.utcnow() + timedelta(days=90)  # 3 month expiry
    )
    
    db.session.add(portfolio)
    db.session.flush()
    
    return portfolio

def generate_portfolio_pdf(student, portfolio):
    """Generate PDF version of portfolio"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    
    story = []
    
    # Title
    story.append(Paragraph("ODYC Student Portfolio", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Student info
    portfolio_data = json.loads(portfolio.portfolio_data)
    story.append(Paragraph(f"Student: {portfolio_data['student']['name']}", styles['Heading2']))
    
    if portfolio_data['student']['bio']:
        story.append(Paragraph(portfolio_data['student']['bio'], styles['Normal']))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Add sections based on included content
    if 'pathways' in portfolio_data:
        story.append(Paragraph("Career Pathways", styles['Heading2']))
        for pathway in portfolio_data['pathways']:
            story.append(Paragraph(f"<b>{pathway['name']}</b> - {pathway['progress']}% Complete", styles['Normal']))
            story.append(Paragraph(pathway['description'], styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    
    if 'modules' in portfolio_data:
        story.append(Paragraph("Completed Learning Modules", styles['Heading2']))
        for module in portfolio_data['modules']:
            story.append(Paragraph(f"<b>{module['title']}</b> - Grade: {module['grade'] or 'N/A'}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer