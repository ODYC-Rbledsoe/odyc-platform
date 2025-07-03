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
