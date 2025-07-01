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
    
    # Relationships
    student_matches = db.relationship('Match', foreign_keys='Match.student_id', backref='student', lazy='dynamic')
    mentor_matches = db.relationship('Match', foreign_keys='Match.mentor_id', backref='mentor', lazy='dynamic')
    
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

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, paused
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='match', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Match {self.student.name} - {self.mentor.name}>'

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
