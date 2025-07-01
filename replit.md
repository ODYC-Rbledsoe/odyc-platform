# Mentorship Platform

## Overview

This is a Flask-based mentorship platform that connects students with mentors for learning and professional development. The platform provides role-based access control with three distinct user types: students, mentors, and administrators. The system facilitates mentor-student matching, session logging, and progress tracking.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLite (development) with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Forms**: WTForms with Flask-WTF for form handling and CSRF protection
- **Password Security**: Werkzeug password hashing

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome 6.0
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### Database Schema
The application uses three main entities:
- **User**: Stores user information including name, email, password hash, role, bio, and interests/expertise
- **Match**: Represents the connection between a student and mentor
- **Session**: Records individual mentoring sessions with topics, notes, and reflections

## Key Components

### Authentication System (`auth.py`)
- User registration with role selection (student/mentor)
- Login/logout functionality with session management
- Password hashing for security
- Automatic redirection based on authentication status

### Dashboard System (`dashboard.py`)
- Role-based dashboard routing
- Student dashboard: View assigned mentor and session history
- Mentor dashboard: Manage multiple students and log sessions
- Profile management functionality

### Admin Panel (`admin.py`)
- Administrative oversight and platform statistics
- User management capabilities
- Match creation and management
- System analytics and reporting

### Forms (`forms.py`)
- Registration form with validation
- Login form
- Session logging form with date/time picker
- Match creation form for admins
- Profile editing form

### Data Models (`models.py`)
- User model with role-based methods
- Match model linking students and mentors
- Session model for tracking mentoring activities
- Proper foreign key relationships and cascading deletes

## Data Flow

1. **User Registration**: New users register with role selection (student/mentor)
2. **Authentication**: Users log in and are redirected to role-appropriate dashboards
3. **Matching**: Admins create matches between students and mentors
4. **Session Management**: Mentors log sessions with their assigned students
5. **Progress Tracking**: Both parties can view session history and progress

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: User session management
- Flask-WTF: Form handling with CSRF protection
- WTForms: Form validation
- Werkzeug: Password hashing and security utilities

### Frontend Libraries
- Bootstrap 5: UI framework with dark theme
- Font Awesome: Icon library
- Custom CSS: Platform-specific styling

## Deployment Strategy

### Development Configuration
- SQLite database for local development
- Debug mode enabled
- Development secret key (should be changed for production)
- Host: 0.0.0.0, Port: 5000

### Production Considerations
- Environment-based configuration using `DATABASE_URL` and `SESSION_SECRET`
- ProxyFix middleware for proper header handling behind reverse proxies
- Database connection pooling with recycle and ping settings
- CSRF protection enabled

### Database Migration Strategy
- SQLAlchemy model-first approach
- Manual database initialization required
- Future migrations should use Flask-Migrate

## Changelog
- July 01, 2025: Complete Flask mentorship platform deployed successfully
  - Full authentication system with role-based access control
  - Student, mentor, and admin dashboards working
  - Match creation and session logging functionality
  - Bootstrap dark theme with professional styling
  - PostgreSQL database integration
  - All core features tested and verified

## User Preferences

Preferred communication style: Simple, everyday language.