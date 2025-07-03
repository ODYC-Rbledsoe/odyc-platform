from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
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
        ('coordinator', 'Mentor Coordinator')
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
