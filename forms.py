from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
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
