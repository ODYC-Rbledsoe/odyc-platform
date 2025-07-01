#!/usr/bin/env python3
"""
Sample data seeder for the Mentorship Platform
Creates demo users, matches, and sessions for testing and demonstration
"""

from app import app, db
from models import User, Match, Session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        print("Creating sample data for Mentorship Platform...")
        
        # Sample students
        students_data = [
            {
                'name': 'Alice Johnson',
                'email': 'alice.johnson@student.com',
                'bio': 'Computer Science student passionate about web development and AI. Looking to learn industry best practices.',
                'interests_expertise': 'Web Development, Python, Machine Learning, React'
            },
            {
                'name': 'Bob Chen',
                'email': 'bob.chen@student.com',
                'bio': 'Engineering student interested in software architecture and system design. Eager to gain real-world experience.',
                'interests_expertise': 'System Design, Java, Cloud Computing, Microservices'
            },
            {
                'name': 'Carol Rodriguez',
                'email': 'carol.rodriguez@student.com',
                'bio': 'Data Science student with a background in statistics. Wants to transition into tech industry.',
                'interests_expertise': 'Data Science, Statistics, Python, SQL, Tableau'
            },
            {
                'name': 'David Kim',
                'email': 'david.kim@student.com',
                'bio': 'Recent bootcamp graduate looking for guidance in mobile app development and career transition.',
                'interests_expertise': 'Mobile Development, React Native, iOS, Android, Career Change'
            },
            {
                'name': 'Emma Wilson',
                'email': 'emma.wilson@student.com',
                'bio': 'Psychology major exploring UX/UI design. Interested in human-computer interaction.',
                'interests_expertise': 'UX/UI Design, Psychology, Figma, User Research, Prototyping'
            }
        ]
        
        # Sample mentors
        mentors_data = [
            {
                'name': 'Dr. Sarah Mitchell',
                'email': 'sarah.mitchell@mentor.com',
                'bio': 'Senior Software Engineer at Google with 8 years of experience in full-stack development and team leadership.',
                'interests_expertise': 'Full-Stack Development, Python, JavaScript, Team Leadership, System Architecture'
            },
            {
                'name': 'Michael Thompson',
                'email': 'michael.thompson@mentor.com',
                'bio': 'Data Science Manager at Netflix. Passionate about mentoring the next generation of data scientists.',
                'interests_expertise': 'Data Science, Machine Learning, Python, R, Analytics, Team Management'
            },
            {
                'name': 'Jennifer Lee',
                'email': 'jennifer.lee@mentor.com',
                'bio': 'Senior UX Designer at Apple with expertise in mobile design and user research methodologies.',
                'interests_expertise': 'UX/UI Design, Mobile Design, User Research, Design Systems, Figma'
            },
            {
                'name': 'Robert Jackson',
                'email': 'robert.jackson@mentor.com',
                'bio': 'Senior Mobile Developer and Tech Lead with 6 years building iOS and Android applications.',
                'interests_expertise': 'Mobile Development, iOS, Android, React Native, Swift, Kotlin'
            }
        ]
        
        created_students = []
        created_mentors = []
        
        # Create students
        for student_data in students_data:
            if not User.query.filter_by(email=student_data['email']).first():
                student = User(
                    name=student_data['name'],
                    email=student_data['email'],
                    password_hash=generate_password_hash('student123'),
                    role='student',
                    bio=student_data['bio'],
                    interests_expertise=student_data['interests_expertise']
                )
                db.session.add(student)
                created_students.append(student)
                print(f"Created student: {student.name}")
        
        # Create mentors
        for mentor_data in mentors_data:
            if not User.query.filter_by(email=mentor_data['email']).first():
                mentor = User(
                    name=mentor_data['name'],
                    email=mentor_data['email'],
                    password_hash=generate_password_hash('mentor123'),
                    role='mentor',
                    bio=mentor_data['bio'],
                    interests_expertise=mentor_data['interests_expertise']
                )
                db.session.add(mentor)
                created_mentors.append(mentor)
                print(f"Created mentor: {mentor.name}")
        
        db.session.commit()
        
        # Create matches
        matches_to_create = [
            (0, 0),  # Alice -> Dr. Sarah (Web Dev)
            (1, 0),  # Bob -> Dr. Sarah (System Design)
            (2, 1),  # Carol -> Michael (Data Science)
            (3, 3),  # David -> Robert (Mobile Dev)
            (4, 2),  # Emma -> Jennifer (UX/UI)
        ]
        
        created_matches = []
        for student_idx, mentor_idx in matches_to_create:
            if student_idx < len(created_students) and mentor_idx < len(created_mentors):
                # Check if match already exists
                existing_match = Match.query.filter_by(
                    student_id=created_students[student_idx].id,
                    mentor_id=created_mentors[mentor_idx].id
                ).first()
                
                if not existing_match:
                    match = Match(
                        student_id=created_students[student_idx].id,
                        mentor_id=created_mentors[mentor_idx].id,
                        status='active',
                        start_date=datetime.utcnow() - timedelta(days=random.randint(30, 90))
                    )
                    db.session.add(match)
                    created_matches.append(match)
                    print(f"Created match: {created_students[student_idx].name} <-> {created_mentors[mentor_idx].name}")
        
        db.session.commit()
        
        # Create sample sessions for each match
        session_topics = [
            "Introduction and Goal Setting",
            "Career Path Planning",
            "Technical Skills Assessment",
            "Project Code Review",
            "Interview Preparation",
            "Industry Best Practices",
            "Portfolio Development",
            "Networking Strategies",
            "Technical Deep Dive",
            "Problem Solving Session",
            "Mock Technical Interview",
            "Professional Development"
        ]
        
        for match in created_matches:
            # Create 2-5 sessions per match
            num_sessions = random.randint(2, 5)
            
            for i in range(num_sessions):
                session_date = match.start_date + timedelta(days=random.randint(7, 60))
                topic = random.choice(session_topics)
                
                session = Session(
                    match_id=match.id,
                    date=session_date,
                    topic=topic,
                    notes=f"Discussed {topic.lower()} with {match.student.name}. Covered key concepts and provided practical guidance. Next steps identified for continued growth.",
                    student_reflection=f"Great session on {topic.lower()}! Learned valuable insights and feel more confident about my progress. Looking forward to applying what we discussed."
                )
                db.session.add(session)
                print(f"Created session: {topic} for {match.student.name}")
        
        db.session.commit()
        
        print("\nSample data creation completed!")
        print("\nDemo Credentials:")
        print("Admin: admin@mentorship.com / admin123")
        print("Students: [name]@student.com / student123")
        print("Mentors: [name]@mentor.com / mentor123")
        print("\nExample student login: alice.johnson@student.com / student123")
        print("Example mentor login: sarah.mitchell@mentor.com / mentor123")

if __name__ == '__main__':
    create_sample_data()