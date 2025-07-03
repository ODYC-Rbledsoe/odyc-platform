from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, SubmitField, IntegerField, BooleanField
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
