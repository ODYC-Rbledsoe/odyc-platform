# ODYC - Mentorship and Workforce Development Platform

## Overview

ODYC is a mentorship and workforce development platform modeled after the Southwest Wyoming Manufacturing Partnership — a coalition built on the principle of being industry-led and community-supported. The platform connects high school students with industry professionals to explore careers, build employability skills, and form meaningful connections that keep talent in Southwest Wyoming.

**Mission**: Transform regional workforce development by creating personalized career roadmaps built around real-world job roles identified by local employers, while providing a scalable mentorship engine that will evolve into a community-connected talent platform.

**Current Focus**: Industry professionals mentor groups of 5-6 students through structured curriculum that builds both technical and professional skills aligned to local industry needs.

**Future Vision**: A comprehensive talent pipeline where industry partners invest in early talent development, access skilled candidates, and reduce hiring risk through education-to-employment pathways.

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
- July 10, 2025: Updated trusted partners section in landing page
  - Changed "Memorial Hospital" to "Sweetwater Memorial" for healthcare services
  - Updated manufacturing section to "Manufacturing & Mining" with partners "WeSoda, Tata, Church & Dwight, Simplot"
  - Added Union Wireless as telecommunications partner with signal icon
  - Added Green River High School as education partner alongside WWCC and Rock Springs High School
  - Reorganized industry partner layout to accommodate 5 partners in balanced grid
- July 06, 2025: Created professional landing page for ODYC platform
  - Built comprehensive homepage showcasing Southwest Wyoming workforce development mission
  - Added value propositions for students, mentors, employers, and schools
  - Featured authentic Southwest Wyoming career pathways with salary data and local job projections
  - Included industry partner showcase (Genesis Alkali, Bridger Coal, Memorial Hospital, Wyoming Machine Works)
  - Implemented responsive design with clear calls-to-action for registration and employer partnerships
  - Added smooth scrolling navigation and professional branding aligned with ODYC identity
  - Integrated authentication flow with seamless transitions to platform features

- July 03, 2025: Implemented comprehensive employer portal features
  - Built complete employer portal with dashboard, profile management, and opportunity posting
  - Added tiered sponsorship model (Bronze $2.5K, Silver $7.5K, Gold $15K, Platinum $25K)
  - Implemented student portfolio generation with PDF export and secure sharing
  - Created employer opportunity management with application tracking system
  - Added anonymized student progress viewing for sponsors
  - Built student application system for employer opportunities
  - Enhanced navigation with employer portal dropdown menu
  - Integrated employer registration flow with industry alignment
  - Created comprehensive seed data with 4 authentic Southwest Wyoming employers
  - Added PDF generation library for professional student portfolios

- July 03, 2025: Transformed platform to reflect ODYC workforce development vision
  - Added career pathway models: Industry, JobRole, CareerPathway, StudentCareerInterest, EmployerPartner
  - Created authentic Southwest Wyoming industry data with 5 industries, 7 job roles, 4 career pathways
  - Built detailed career roadmaps based on WWCC and RSHS programs:
    * Electrical & Instrumentation Technician (6 skill milestones, OSHA-10, ISA standards)
    * Process Operator (Hazmat certification, emergency response, Genesis Alkali partnership)
    * Mechanical Maintenance Technician (hydraulics/pneumatics, CMMS, preventive maintenance)
  - Integrated real employer partnerships: Genesis Alkali, Bridger Coal, Memorial Hospital
  - Added career exploration and pathway tracking for students
  - Updated branding to "ODYC - Southwest Wyoming Workforce Development"
  - Enhanced navigation with industry-focused messaging and career journey tracking
  - Linked curriculum modules to specific career pathways with dual enrollment options

- July 03, 2025: Added comprehensive curriculum management system
  - Created curriculum models: CurriculumModule, GroupProgress, StudentProgress
  - Built curriculum management interface for admins
  - Added mentor curriculum delivery system
  - Created student learning interface with assignment submission
  - Implemented group mentoring system with 5-6 students per mentor
  - Added group management features for admins
  - Seeded system with 4 comprehensive curriculum modules
  - Updated navigation with role-based curriculum access

- July 01, 2025: Complete Flask mentorship platform deployed successfully
  - Full authentication system with role-based access control
  - Student, mentor, admin, and coordinator dashboards working
  - Match creation and session logging functionality
  - Bootstrap dark theme with professional styling
  - PostgreSQL database integration
  - All core features tested and verified
  - Added coordinator role for session scheduling and management

## User Preferences

Preferred communication style: Simple, everyday language.