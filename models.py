from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, mentor, coordinator, admin
    bio = db.Column(db.Text)
    interests_expertise = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships will be defined via backref in other models
    
    def __repr__(self):
        return f'<User {self.name} ({self.role})>'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_mentor(self):
        return self.role == 'mentor'
    
    def is_student(self):
        return self.role == 'student'
    
    def is_coordinator(self):
        return self.role == 'coordinator'

class MentorGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Group name like "Spring 2025 - Data Science"
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, paused
    max_students = db.Column(db.Integer, default=6)  # Maximum students per group
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='mentor_groups')
    
    def __repr__(self):
        return f'<MentorGroup {self.name}>'
    
    @property
    def student_count(self):
        return GroupMembership.query.filter_by(group_id=self.id, status='active').count()
    
    @property
    def students(self):
        memberships = GroupMembership.query.filter_by(group_id=self.id, status='active').all()
        return [membership.student for membership in memberships]

class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('mentor_group.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, dropped
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('MentorGroup', backref='memberships')
    student = db.relationship('User', foreign_keys=[student_id], backref='group_memberships')
    
    def __repr__(self):
        return f'<GroupMembership {self.student.name} in {self.group.name}>'

# Keep the old Match model for backward compatibility during transition
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, paused
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='match', lazy='dynamic', cascade='all, delete-orphan')
    student = db.relationship('User', foreign_keys=[student_id], backref='student_matches')
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='mentor_matches')
    
    def __repr__(self):
        return f'<Match {self.student.name} - {self.mentor.name}>'

class GroupSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('mentor_group.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    topic = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, default=60)  # Session duration
    attendees_count = db.Column(db.Integer, default=0)  # Number of students who attended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('MentorGroup', backref='sessions')
    
    def __repr__(self):
        return f'<GroupSession {self.topic} on {self.date.strftime("%Y-%m-%d")}>'
    
    @property
    def attendance_rate(self):
        if self.group.student_count == 0:
            return 0
        return (self.attendees_count / self.group.student_count) * 100

class StudentReflection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('group_session.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reflection = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 rating of the session
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    session = db.relationship('GroupSession', backref='student_reflections')
    student = db.relationship('User', backref='session_reflections')
    
    def __repr__(self):
        return f'<StudentReflection by {self.student.name} for session {self.session_id}>'

class CurriculumModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)  # Main curriculum content
    order_index = db.Column(db.Integer, default=0)  # For ordering modules
    duration_weeks = db.Column(db.Integer, default=1)  # Expected duration to complete
    difficulty_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    learning_objectives = db.Column(db.Text)  # What students will learn
    resources = db.Column(db.Text)  # Additional resources, links, etc.
    assignments = db.Column(db.Text)  # Homework/assignments for students
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CurriculumModule {self.title}>'

class GroupProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('mentor_group.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('curriculum_module.id'), nullable=False)
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    started_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    mentor_notes = db.Column(db.Text)  # Mentor's notes on group progress
    
    # Relationships
    group = db.relationship('MentorGroup', backref='curriculum_progress')
    module = db.relationship('CurriculumModule', backref='group_progress')
    
    def __repr__(self):
        return f'<GroupProgress {self.group.name} - {self.module.title}>'

class StudentProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('curriculum_module.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('mentor_group.id'), nullable=False)
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    completion_percentage = db.Column(db.Integer, default=0)  # 0-100%
    assignment_submitted = db.Column(db.Boolean, default=False)
    assignment_content = db.Column(db.Text)  # Student's assignment submission
    mentor_feedback = db.Column(db.Text)  # Mentor's feedback on student work
    grade = db.Column(db.String(10))  # A, B, C, D, F or Pass/Fail
    started_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    
    # Relationships
    student = db.relationship('User', backref='curriculum_progress')
    module = db.relationship('CurriculumModule', backref='student_progress')
    group = db.relationship('MentorGroup')
    
    def __repr__(self):
        return f'<StudentProgress {self.student.name} - {self.module.title}>'

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Manufacturing, Healthcare, Energy, etc.
    description = db.Column(db.Text)
    region = db.Column(db.String(100), default='Southwest Wyoming')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Industry {self.name}>'

class JobRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Electrical & Instrumentation Technician
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)  # Skills, education, certifications needed
    salary_range = db.Column(db.String(50))  # $45,000 - $65,000
    growth_outlook = db.Column(db.String(20))  # High, Medium, Low
    local_demand = db.Column(db.Integer, default=0)  # Number of projected openings
    education_level = db.Column(db.String(50))  # High School, Associate, Bachelor's, etc.
    is_priority = db.Column(db.Boolean, default=False)  # High-demand local roles
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    industry = db.relationship('Industry', backref='job_roles')
    
    def __repr__(self):
        return f'<JobRole {self.title}>'

class CareerPathway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Manufacturing Technician Pathway
    description = db.Column(db.Text)
    job_role_id = db.Column(db.Integer, db.ForeignKey('job_role.id'), nullable=False)
    duration_months = db.Column(db.Integer, default=12)  # Expected pathway completion time
    prerequisites = db.Column(db.Text)  # What students need before starting
    career_outcomes = db.Column(db.Text)  # Expected career outcomes
    employer_partners = db.Column(db.Text)  # Companies supporting this pathway
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    job_role = db.relationship('JobRole', backref='career_pathways')
    
    def __repr__(self):
        return f'<CareerPathway {self.name}>'

class PathwayModule(db.Model):
    """Links curriculum modules to career pathways with specific ordering"""
    id = db.Column(db.Integer, primary_key=True)
    pathway_id = db.Column(db.Integer, db.ForeignKey('career_pathway.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('curriculum_module.id'), nullable=False)
    order_in_pathway = db.Column(db.Integer, default=1)
    is_required = db.Column(db.Boolean, default=True)
    estimated_completion_weeks = db.Column(db.Integer, default=2)
    
    # Relationships
    pathway = db.relationship('CareerPathway', backref='pathway_modules')
    module = db.relationship('CurriculumModule', backref='pathway_associations')
    
    def __repr__(self):
        return f'<PathwayModule {self.pathway.name} - {self.module.title}>'

class StudentCareerInterest(db.Model):
    """Tracks student interest in career pathways and job roles"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pathway_id = db.Column(db.Integer, db.ForeignKey('career_pathway.id'), nullable=False)
    interest_level = db.Column(db.String(20), default='interested')  # interested, exploring, committed
    progress_percentage = db.Column(db.Integer, default=0)  # 0-100% through pathway
    started_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_completion = db.Column(db.DateTime)
    mentor_notes = db.Column(db.Text)
    
    # Relationships
    student = db.relationship('User', backref='career_interests')
    pathway = db.relationship('CareerPathway', backref='interested_students')
    
    def __repr__(self):
        return f'<StudentCareerInterest {self.student.name} - {self.pathway.name}>'

class EmployerPartner(db.Model):
    """Local employers participating in workforce development"""
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'), nullable=False)
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    website = db.Column(db.String(200))
    employee_count = db.Column(db.String(50))  # 1-10, 11-50, 51-200, etc.
    participation_level = db.Column(db.String(50))  # Mentor Provider, Hiring Partner, Full Partner
    hiring_needs = db.Column(db.Text)  # Current and projected hiring needs
    mentors_provided = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    industry = db.relationship('Industry', backref='employer_partners')
    
    def __repr__(self):
        return f'<EmployerPartner {self.company_name}>'

# Keep the old Session model for backward compatibility
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    topic = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    student_reflection = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Session {self.topic} on {self.date.strftime("%Y-%m-%d")}>'
