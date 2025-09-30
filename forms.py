from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, SubmitField, IntegerField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, URL, Optional
from wtforms.widgets import DateTimeLocalInput
from datetime import datetime

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('coordinator', 'Mentor Coordinator'),
        ('employer', 'Employer Partner')
    ], validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    interests_expertise = TextAreaField('Interests/Expertise', validators=[Length(max=500)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SessionForm(FlaskForm):
    date = DateTimeField('Session Date', validators=[DataRequired()], 
                        widget=DateTimeLocalInput(), default=datetime.now)
    topic = StringField('Topic', validators=[DataRequired(), Length(max=200)])
    notes = TextAreaField('Notes')
    student_reflection = TextAreaField('Student Reflection')
    submit = SubmitField('Log Session')

class MatchForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    mentor_id = SelectField('Mentor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Match')

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    interests_expertise = TextAreaField('Interests/Expertise', validators=[Length(max=500)])
    submit = SubmitField('Update Profile')

class ScheduleSessionForm(FlaskForm):
    match_id = SelectField('Match', coerce=int, validators=[DataRequired()])
    date = DateTimeField('Session Date', validators=[DataRequired()], 
                        widget=DateTimeLocalInput(), default=datetime.now)
    topic = StringField('Topic', validators=[DataRequired(), Length(max=200)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Schedule Session')

class CreateGroupForm(FlaskForm):
    mentor_id = SelectField('Mentor', coerce=int, validators=[DataRequired()])
    name = StringField('Group Name', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    max_students = SelectField('Maximum Students', coerce=int, choices=[
        (4, '4 Students'), (5, '5 Students'), (6, '6 Students'), (7, '7 Students'), (8, '8 Students')
    ], default=6, validators=[DataRequired()])
    submit = SubmitField('Create Group')

class AddStudentToGroupForm(FlaskForm):
    group_id = SelectField('Mentor Group', coerce=int, validators=[DataRequired()])
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Student to Group')

class GroupSessionForm(FlaskForm):
    date = DateTimeField('Session Date', validators=[DataRequired()], 
                        widget=DateTimeLocalInput(), default=datetime.now)
    topic = StringField('Topic', validators=[DataRequired(), Length(max=200)])
    notes = TextAreaField('Session Notes')
    duration_minutes = SelectField('Duration (minutes)', coerce=int, choices=[
        (30, '30 minutes'), (45, '45 minutes'), (60, '1 hour'), 
        (90, '1.5 hours'), (120, '2 hours')
    ], default=60, validators=[DataRequired()])
    attendees_count = IntegerField('Number of Attendees', validators=[DataRequired(), NumberRange(min=0, max=8)])
    submit = SubmitField('Log Group Session')

class StudentReflectionForm(FlaskForm):
    reflection = TextAreaField('Your Reflection', validators=[DataRequired(), Length(max=1000)])
    rating = SelectField('Session Rating', coerce=int, choices=[
        (1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Reflection')

class CurriculumModuleForm(FlaskForm):
    title = StringField('Module Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    content = TextAreaField('Main Content', validators=[DataRequired()], 
                           render_kw={"rows": 10, "placeholder": "Enter the main curriculum content..."})
    learning_objectives = TextAreaField('Learning Objectives', validators=[Length(max=1000)],
                                      render_kw={"placeholder": "What will students learn from this module?"})
    resources = TextAreaField('Additional Resources', validators=[Length(max=1000)],
                            render_kw={"placeholder": "Links, books, videos, or other learning materials"})
    assignments = TextAreaField('Assignments', validators=[Length(max=1000)],
                              render_kw={"placeholder": "Homework, projects, or tasks for students"})
    duration_weeks = SelectField('Duration (weeks)', coerce=int, choices=[
        (1, '1 week'), (2, '2 weeks'), (3, '3 weeks'), (4, '4 weeks'), 
        (6, '6 weeks'), (8, '8 weeks'), (12, '12 weeks')
    ], default=1, validators=[DataRequired()])
    difficulty_level = SelectField('Difficulty Level', choices=[
        ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')
    ], default='beginner', validators=[DataRequired()])
    order_index = IntegerField('Order (for sequencing)', validators=[DataRequired()], default=1)
    submit = SubmitField('Save Module')

class AssignmentSubmissionForm(FlaskForm):
    assignment_content = TextAreaField('Your Assignment', validators=[DataRequired(), Length(max=5000)],
                                     render_kw={"rows": 8, "placeholder": "Submit your completed assignment..."})
    submit = SubmitField('Submit Assignment')

class GradingForm(FlaskForm):
    grade = SelectField('Grade', choices=[
        ('A', 'A - Excellent'), ('B', 'B - Good'), ('C', 'C - Satisfactory'), 
        ('D', 'D - Needs Improvement'), ('F', 'F - Unsatisfactory'),
        ('Pass', 'Pass'), ('Fail', 'Fail')
    ], validators=[DataRequired()])
    mentor_feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(max=1000)],
                                  render_kw={"placeholder": "Provide constructive feedback on the student's work..."})
    submit = SubmitField('Submit Grade & Feedback')

class GroupProgressForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')
    ], validators=[DataRequired()])
    mentor_notes = TextAreaField('Notes', validators=[Length(max=1000)],
                                render_kw={"placeholder": "Add notes about the group's progress..."})
    submit = SubmitField('Update Progress')

# Employer Portal Forms
class EmployerRegistrationForm(FlaskForm):
    # User account fields
    name = StringField('Your Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Business Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')])
    
    # Company fields
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=200)])
    industry_id = SelectField('Industry', coerce=int, validators=[DataRequired()])
    contact_phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    website = StringField('Company Website', validators=[Optional(), URL(), Length(max=200)])
    address = TextAreaField('Company Address', validators=[Optional(), Length(max=500)])
    employee_count = SelectField('Company Size', choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('500+', '500+ employees')
    ], validators=[DataRequired()])
    
    # Business needs
    description = TextAreaField('Company Description', validators=[Optional(), Length(max=1000)],
                               render_kw={"placeholder": "Brief description of your company for students..."})
    hiring_needs = TextAreaField('Current Hiring Needs', validators=[Optional(), Length(max=1000)],
                                render_kw={"placeholder": "Describe your current and projected hiring needs..."})
    annual_hires = IntegerField('Annual Hires (projected)', validators=[Optional(), NumberRange(min=0, max=1000)])
    
    submit = SubmitField('Register Company')

class EmployerProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=200)])
    industry_id = SelectField('Industry', coerce=int, validators=[DataRequired()])
    contact_name = StringField('Primary Contact', validators=[DataRequired(), Length(min=2, max=100)])
    contact_phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    website = StringField('Company Website', validators=[Optional(), URL(), Length(max=200)])
    address = TextAreaField('Company Address', validators=[Optional(), Length(max=500)])
    
    description = TextAreaField('Company Description', validators=[Optional(), Length(max=1000)],
                               render_kw={"rows": 4, "placeholder": "Tell students about your company..."})
    company_culture = TextAreaField('Company Culture', validators=[Optional(), Length(max=1000)],
                                   render_kw={"rows": 3, "placeholder": "Describe your workplace culture..."})
    benefits_offered = TextAreaField('Benefits & Compensation', validators=[Optional(), Length(max=1000)],
                                    render_kw={"rows": 3, "placeholder": "Benefits, salary ranges, perks..."})
    
    hiring_needs = TextAreaField('Hiring Needs', validators=[Optional(), Length(max=1000)],
                                render_kw={"rows": 4, "placeholder": "Current and projected hiring needs..."})
    annual_hires = IntegerField('Annual Hires', validators=[Optional(), NumberRange(min=0, max=1000)])
    internship_capacity = IntegerField('Internship Positions Available', validators=[Optional(), NumberRange(min=0, max=100)])
    mentor_capacity = IntegerField('Available Mentors', validators=[Optional(), NumberRange(min=0, max=50)])
    
    submit = SubmitField('Update Profile')

class OpportunityForm(FlaskForm):
    title = StringField('Opportunity Title', validators=[DataRequired(), Length(min=5, max=200)])
    opportunity_type = SelectField('Type', choices=[
        ('internship', 'Internship'),
        ('apprenticeship', 'Apprenticeship'),
        ('job_shadow', 'Job Shadow'),
        ('mentorship', 'Mentorship Program'),
        ('entry_level', 'Entry Level Position')
    ], validators=[DataRequired()])
    
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=50, max=2000)],
                               render_kw={"rows": 6, "placeholder": "Detailed description of the opportunity..."})
    requirements = TextAreaField('Requirements', validators=[Optional(), Length(max=1000)],
                                render_kw={"rows": 4, "placeholder": "Prerequisites, skills, education requirements..."})
    
    pathway_id = SelectField('Target Career Pathway', coerce=int, validators=[Optional()])
    duration = StringField('Duration', validators=[Optional(), Length(max=100)],
                          render_kw={"placeholder": "e.g., 10 weeks, 6 months, ongoing"})
    compensation = StringField('Compensation', validators=[Optional(), Length(max=100)],
                              render_kw={"placeholder": "e.g., $15/hour, Unpaid, $500 stipend"})
    
    positions_available = IntegerField('Positions Available', validators=[DataRequired(), NumberRange(min=1, max=100)])
    application_deadline = DateTimeField('Application Deadline', validators=[Optional()],
                                        widget=DateTimeLocalInput())
    start_date = DateTimeField('Start Date', validators=[Optional()], widget=DateTimeLocalInput())
    end_date = DateTimeField('End Date', validators=[Optional()], widget=DateTimeLocalInput())
    
    submit = SubmitField('Post Opportunity')

class SponsorshipForm(FlaskForm):
    tier = SelectField('Sponsorship Tier', choices=[
        ('bronze', 'Bronze - Basic Partner ($2,500/year)'),
        ('silver', 'Silver - Talent Partner ($7,500/year)'),
        ('gold', 'Gold - Strategic Partner ($15,000/year)'),
        ('platinum', 'Platinum - Premier Partner ($25,000/year)')
    ], validators=[DataRequired()])
    
    pathway_focus = SelectField('Primary Pathway Interest', coerce=int, validators=[Optional()])
    branding_interest = BooleanField('Company branding on student materials')
    early_access = BooleanField('Early access to graduating students')
    curriculum_input = BooleanField('Input on curriculum development')
    exclusive_events = BooleanField('Exclusive networking events')
    
    contact_name = StringField('Billing Contact', validators=[DataRequired(), Length(min=2, max=100)])
    contact_email = StringField('Billing Email', validators=[DataRequired(), Email()])
    
    notes = TextAreaField('Additional Requests', validators=[Optional(), Length(max=1000)],
                         render_kw={"placeholder": "Any specific needs or requests..."})
    
    submit = SubmitField('Submit Sponsorship Request')

class StudentExportForm(FlaskForm):
    include_personal = BooleanField('Include Personal Information', default=True)
    include_pathway = BooleanField('Include Career Pathway Progress', default=True)
    include_curriculum = BooleanField('Include Learning Modules', default=True)
    include_sessions = BooleanField('Include Mentoring Sessions', default=True)
    include_achievements = BooleanField('Include Certifications & Achievements', default=True)
    include_recommendations = BooleanField('Include Mentor Recommendations', default=False)
    
    export_format = SelectField('Export Format', choices=[
        ('pdf', 'PDF Portfolio'),
        ('digital', 'Digital Profile Link'),
        ('both', 'PDF + Digital Link')
    ], default='pdf', validators=[DataRequired()])
    
    recipient_email = StringField('Share with Employer (Optional)', validators=[Optional(), Email()],
                                 render_kw={"placeholder": "employer@company.com"})
    
    submit = SubmitField('Generate Portfolio')

# Career Cluster Management Forms
class ClusterForm(FlaskForm):
    name = StringField('Cluster Name', validators=[DataRequired(), Length(min=2, max=100)],
                      render_kw={"placeholder": "e.g., Advanced Manufacturing"})
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)],
                               render_kw={"rows": 4, "placeholder": "Detailed description of this career cluster..."})
    color_code = StringField('Color Code', validators=[Optional(), Length(max=7)],
                            render_kw={"placeholder": "#FF6B35", "type": "color"})
    icon_class = StringField('Icon Class', validators=[Optional(), Length(max=50)],
                           render_kw={"placeholder": "fas fa-industry"})
    is_cross_cutting = BooleanField('Cross-Cutting Skills', 
                                   description="Mark if this represents cross-cutting skills like Digital Technology")
    is_priority_local = BooleanField('Local Priority', 
                                   description="High priority for Southwest Wyoming region")
    is_active = BooleanField('Active', default=True, description="Deactivate to hide from students")
    sort_order = IntegerField('Sort Order', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    submit = SubmitField('Save Cluster')

class PathwayClusterMappingForm(FlaskForm):
    pathway_id = SelectField('Career Pathway', coerce=int, validators=[DataRequired()])
    cluster_id = SelectField('Career Cluster', coerce=int, validators=[DataRequired()])
    is_primary = BooleanField('Primary Association', default=True,
                            description="Primary vs secondary cluster association")
    submit = SubmitField('Add Mapping')

# Pathway Workshop Forms
class ProjectCardForm(FlaskForm):
    """Form for employers and educators to co-author project cards"""
    pathway_id = SelectField('Career Pathway', coerce=int, validators=[DataRequired()],
                            render_kw={"class": "form-select"})
    title = StringField('Project Title', validators=[DataRequired(), Length(min=5, max=200)],
                       render_kw={"placeholder": "e.g., Lockout/Tagout Walkdown"})
    objective = TextAreaField('Learning Objective', validators=[DataRequired(), Length(min=20, max=1000)],
                             render_kw={"rows": 3, "placeholder": "What will students accomplish through this project?"})
    duration_hours = SelectField('Duration (hours)', coerce=int, choices=[
        (2, '2 hours'), (4, '4 hours'), (6, '6 hours'), (8, '8 hours'),
        (10, '10 hours'), (12, '12 hours'), (16, '16 hours'), (20, '20 hours')
    ], default=4, validators=[DataRequired()])
    
    # Prerequisites and steps
    prerequisites = TextAreaField('Prerequisites', validators=[Optional(), Length(max=1000)],
                                 render_kw={"rows": 2, "placeholder": "Site orientation; OSHA-10; PPE training (one per line)"})
    steps = TextAreaField('Step-by-Step Instructions', validators=[DataRequired(), Length(min=20, max=2000)],
                         render_kw={"rows": 5, "placeholder": "Step 1: Identify energy sources\nStep 2: Verify procedures\nStep 3: Apply locks..."})
    
    # Safety and materials
    safety_notes = TextAreaField('Safety & JHA Notes', validators=[Optional(), Length(max=1000)],
                                render_kw={"rows": 3, "placeholder": "OSHA requirements, hazards, emergency procedures..."})
    tools_materials = TextAreaField('Tools & Materials', validators=[Optional(), Length(max=1000)],
                                   render_kw={"rows": 2, "placeholder": "Hard hat, safety glasses, locks, tags, multimeter..."})
    ppe_required = StringField('PPE Required', validators=[Optional(), Length(max=200)],
                              render_kw={"placeholder": "Hard hat, safety glasses, steel-toe boots, gloves"})
    
    # Artifact specification
    artifact_type = SelectField('Artifact Type', choices=[
        ('checklist+photos', 'Checklist + Photos'),
        ('photos', 'Photos Only'),
        ('video', 'Video Demonstration'),
        ('report', 'Written Report'),
        ('checklist', 'Checklist Only'),
        ('presentation', 'Presentation')
    ], default='checklist+photos', validators=[DataRequired()])
    artifact_description = TextAreaField('What to Submit', validators=[DataRequired(), Length(min=20, max=500)],
                                        render_kw={"rows": 2, "placeholder": "Submit completed checklist with 3-4 photos showing each step..."})
    
    # Logistics
    location_type = SelectField('Location', choices=[
        ('onsite', 'On-site at employer'),
        ('school', 'School-based simulation'),
        ('hybrid', 'Hybrid (both locations)')
    ], default='onsite', validators=[DataRequired()])
    capacity_per_month = IntegerField('Students per Month', validators=[DataRequired(), NumberRange(min=1, max=50)],
                                     default=4, render_kw={"placeholder": "4"})
    mentor_required = BooleanField('Mentor Required', default=True)
    supervisor_signoff = BooleanField('Supervisor Sign-off Required', default=True)
    
    submit = SubmitField('Save Project Card')

class RubricForm(FlaskForm):
    """Form for creating assessment rubrics"""
    pathway_id = SelectField('Career Pathway', coerce=int, validators=[DataRequired()])
    project_card_id = SelectField('Project Card (Optional)', coerce=int, validators=[Optional()])
    
    competency = StringField('Competency', validators=[DataRequired(), Length(min=5, max=200)],
                            render_kw={"placeholder": "e.g., Lockout/Tagout Procedures"})
    
    # Performance levels
    novice_criteria = TextAreaField('Novice Level', validators=[DataRequired(), Length(min=20, max=500)],
                                   render_kw={"rows": 2, "placeholder": "Can identify energy sources with guidance..."})
    developing_criteria = TextAreaField('Developing Level', validators=[DataRequired(), Length(min=20, max=500)],
                                       render_kw={"rows": 2, "placeholder": "Performs LOTO with minor prompts; completes checklist..."})
    proficient_criteria = TextAreaField('Proficient Level', validators=[DataRequired(), Length(min=20, max=500)],
                                       render_kw={"rows": 2, "placeholder": "Executes LOTO independently; verifies try-out; completes documentation..."})
    
    weight = IntegerField('Weight', validators=[Optional(), NumberRange(min=1, max=10)], default=1,
                         render_kw={"placeholder": "1"})
    is_required = BooleanField('Required for Pathway Completion', default=True)
    
    submit = SubmitField('Save Rubric')

class ArtifactSubmissionForm(FlaskForm):
    """Form for students to submit project artifacts"""
    project_card_id = HiddenField(validators=[DataRequired()])
    
    submission_text = TextAreaField('Project Summary', validators=[DataRequired(), Length(min=50, max=2000)],
                                   render_kw={"rows": 5, "placeholder": "Describe what you did, what you learned, and any challenges you faced..."})
    
    # File upload would be handled separately with Flask-Upload or similar
    # For now, we'll use a text field for file paths
    checklist_data = TextAreaField('Checklist Items (Optional)', validators=[Optional(), Length(max=2000)],
                                  render_kw={"rows": 4, "placeholder": "Checked item 1\nChecked item 2\n..."})
    
    submit = SubmitField('Submit Artifact')

class MentorSignoffForm(FlaskForm):
    """Form for mentors to review and approve student artifacts"""
    artifact_id = HiddenField(validators=[DataRequired()])
    
    performance_level = SelectField('Performance Level', choices=[
        ('novice', 'Novice - Needs significant guidance'),
        ('developing', 'Developing - Shows progress, needs minor support'),
        ('proficient', 'Proficient - Demonstrates mastery')
    ], validators=[DataRequired()])
    
    mentor_feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(min=20, max=1000)],
                                   render_kw={"rows": 4, "placeholder": "Provide constructive feedback on the student's work..."})
    
    status = SelectField('Decision', choices=[
        ('approved', 'Approve - Award Badge'),
        ('needs_revision', 'Needs Revision - Return to Student')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Submit Review')

class SkillsBadgeForm(FlaskForm):
    """Form for creating digital badges"""
    name = StringField('Badge Name', validators=[DataRequired(), Length(min=3, max=100)],
                      render_kw={"placeholder": "e.g., LOTO Certified"})
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20, max=500)],
                               render_kw={"rows": 3, "placeholder": "What this badge represents..."})
    icon_class = StringField('Icon Class', validators=[Optional(), Length(max=50)],
                           render_kw={"placeholder": "fas fa-certificate"})
    color_code = StringField('Badge Color', validators=[Optional(), Length(max=7)],
                           render_kw={"type": "color", "value": "#4CAF50"})
    
    pathway_id = SelectField('Career Pathway', coerce=int, validators=[Optional()])
    project_card_id = SelectField('Project Card', coerce=int, validators=[Optional()])
    required_artifacts = IntegerField('Artifacts Required', validators=[DataRequired(), NumberRange(min=1, max=10)],
                                     default=1, render_kw={"placeholder": "1"})
    
    industry_recognized = BooleanField('Industry-Recognized Credential', default=False)
    stackable = BooleanField('Stackable (Can combine with other badges)', default=True)
    
    submit = SubmitField('Create Badge')
