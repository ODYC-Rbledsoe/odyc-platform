"""
Seed file for ODYC Employer Portal
Creates sample employer accounts, opportunities, and sponsorships to demonstrate functionality
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json

def seed_employer_data():
    """Create sample employer accounts and opportunities"""
    
    with app.app_context():
        print("🏢 Seeding employer portal data...")
        
        # Get industries for reference
        manufacturing = Industry.query.filter_by(name="Manufacturing").first()
        energy = Industry.query.filter_by(name="Energy & Mining").first()
        healthcare = Industry.query.filter_by(name="Healthcare").first()
        
        if not manufacturing or not energy or not healthcare:
            print("❌ Industries not found. Please run seed_industry_data.py first")
            return
        
        # Get career pathways
        electrical_pathway = CareerPathway.query.filter_by(name="Electrical & Instrumentation Technician").first()
        process_pathway = CareerPathway.query.filter_by(name="Process Operator").first()
        maintenance_pathway = CareerPathway.query.filter_by(name="Mechanical Maintenance Technician").first()
        
        # Create sample employer users and profiles
        employers_data = [
            {
                'user': {
                    'name': 'Sarah Chen',
                    'email': 'sarah.chen@genesisalkali.com',
                    'password': 'password123',
                    'role': 'employer'
                },
                'company': {
                    'company_name': 'Genesis Alkali',
                    'industry_id': energy.id,
                    'contact_phone': '(307) 382-1000',
                    'website': 'https://genesisalkali.com',
                    'address': '1000 Energy Lane, Green River, WY 82935',
                    'employee_count': '201-500',
                    'description': 'Leading soda ash producer serving global markets. Genesis Alkali is committed to sustainable mining and creating opportunities for local talent in Southwest Wyoming.',
                    'company_culture': 'Safety-first culture with strong emphasis on professional development, environmental stewardship, and community investment.',
                    'benefits_offered': 'Competitive salary ($65K-$95K), full health/dental/vision, 401k match, tuition reimbursement, paid training programs',
                    'hiring_needs': 'Seeking Process Operators, Maintenance Technicians, and Electrical Technicians for expanding operations. Strong demand for OSHA-certified candidates.',
                    'annual_hires': 25,
                    'internship_capacity': 8,
                    'mentor_capacity': 6,
                    'preferred_pathways': json.dumps([process_pathway.id, electrical_pathway.id] if process_pathway and electrical_pathway else [])
                }
            },
            {
                'user': {
                    'name': 'Mike Rodriguez',
                    'email': 'mike.rodriguez@bridgercoal.com',
                    'password': 'password123',
                    'role': 'employer'
                },
                'company': {
                    'company_name': 'Bridger Coal Company',
                    'industry_id': energy.id,
                    'contact_phone': '(307) 352-6400',
                    'website': 'https://bridgercoal.com',
                    'address': '2400 Coal Mine Road, Rock Springs, WY 82901',
                    'employee_count': '501+',
                    'description': 'Major coal mining operation powering regional energy needs. Bridger Coal invests heavily in technology and workforce development.',
                    'company_culture': 'Team-oriented mining professionals focused on safety, innovation, and continuous improvement in mining operations.',
                    'benefits_offered': 'Excellent wages ($70K-$110K), comprehensive benefits, profit sharing, extensive safety training, career advancement',
                    'hiring_needs': 'Heavy equipment operators, maintenance specialists, electrical technicians. Mining experience preferred but will train motivated candidates.',
                    'annual_hires': 35,
                    'internship_capacity': 12,
                    'mentor_capacity': 8,
                    'preferred_pathways': json.dumps([maintenance_pathway.id, electrical_pathway.id] if maintenance_pathway and electrical_pathway else [])
                }
            },
            {
                'user': {
                    'name': 'Dr. Jennifer Walsh',
                    'email': 'jennifer.walsh@sweetwatermemorial.com',
                    'password': 'password123',
                    'role': 'employer'
                },
                'company': {
                    'company_name': 'Sweetwater Memorial Hospital',
                    'industry_id': healthcare.id,
                    'contact_phone': '(307) 362-3711',
                    'website': 'https://sweetwatermemorial.com',
                    'address': '1200 College Drive, Rock Springs, WY 82901',
                    'employee_count': '201-500',
                    'description': 'Leading healthcare provider for Southwest Wyoming, offering comprehensive medical services and committed to training the next generation of healthcare professionals.',
                    'company_culture': 'Patient-centered care with emphasis on professional growth, community health, and collaborative medical practice.',
                    'benefits_offered': 'Competitive healthcare wages, full benefits, tuition assistance, CME funding, flexible scheduling, retirement planning',
                    'hiring_needs': 'Medical technicians, nursing assistants, maintenance staff. Strong partnership with WWCC nursing program.',
                    'annual_hires': 40,
                    'internship_capacity': 15,
                    'mentor_capacity': 10,
                    'preferred_pathways': json.dumps([maintenance_pathway.id] if maintenance_pathway else [])
                }
            },
            {
                'user': {
                    'name': 'Tom Anderson',
                    'email': 'tom.anderson@wyomingmachine.com',
                    'password': 'password123',
                    'role': 'employer'
                },
                'company': {
                    'company_name': 'Wyoming Machine Works',
                    'industry_id': manufacturing.id,
                    'contact_phone': '(307) 382-5500',
                    'website': 'https://wyomingmachine.com',
                    'address': '800 Industrial Blvd, Green River, WY 82935',
                    'employee_count': '51-200',
                    'description': 'Custom manufacturing and machining services supporting mining, energy, and industrial sectors throughout the Rocky Mountain region.',
                    'company_culture': 'Precision craftsmanship culture with strong apprenticeship traditions and focus on advanced manufacturing techniques.',
                    'benefits_offered': 'Skilled trade wages ($55K-$85K), health benefits, apprenticeship programs, tool allowances, overtime opportunities',
                    'hiring_needs': 'Machinists, welders, maintenance technicians. Seeking candidates with mechanical aptitude and willingness to learn precision manufacturing.',
                    'annual_hires': 15,
                    'internship_capacity': 6,
                    'mentor_capacity': 4,
                    'preferred_pathways': json.dumps([maintenance_pathway.id] if maintenance_pathway else [])
                }
            }
        ]
        
        created_employers = []
        
        for employer_data in employers_data:
            # Check if user already exists
            existing_user = User.query.filter_by(email=employer_data['user']['email']).first()
            if existing_user:
                print(f"  ⚠️  User {employer_data['user']['email']} already exists, skipping...")
                continue
                
            # Create user account
            user = User(
                name=employer_data['user']['name'],
                email=employer_data['user']['email'],
                password_hash=generate_password_hash(employer_data['user']['password']),
                role=employer_data['user']['role']
            )
            db.session.add(user)
            db.session.flush()  # Get user ID
            
            # Create employer profile
            employer = EmployerPartner(
                user_id=user.id,
                contact_name=user.name,
                contact_email=user.email,
                **employer_data['company']
            )
            db.session.add(employer)
            db.session.flush()
            
            created_employers.append(employer)
            print(f"  ✅ Created employer: {employer.company_name}")
        
        # Create sample opportunities
        opportunities_data = [
            {
                'employer': 'Genesis Alkali',
                'title': 'Summer Process Operator Internship',
                'opportunity_type': 'internship',
                'description': '''Join our 12-week summer internship program and gain hands-on experience in soda ash production. You'll work alongside experienced Process Operators to learn:

• Plant operations and safety protocols
• Chemical process monitoring and control
• Equipment inspection and maintenance
• Data collection and analysis
• Emergency response procedures

This internship provides real-world exposure to industrial chemistry and process operations. Successful interns often receive full-time offers upon graduation.

Located at our Green River facility, you'll be part of a team that produces soda ash for glass manufacturing, chemicals, and other industries worldwide.''',
                'requirements': '''• Currently enrolled in ODYC Process Operator pathway
• OSHA-10 certification (we can provide if needed)
• Strong mathematical and analytical skills
• Ability to work rotating shifts including weekends
• Pass pre-employment drug screening and physical
• Must be 18+ years old for safety requirements''',
                'pathway': 'Process Operator',
                'duration': '12 weeks (June - August)',
                'compensation': '$18/hour plus overtime',
                'positions_available': 4,
                'application_deadline': datetime.now() + timedelta(days=45),
                'start_date': datetime(2025, 6, 1),
                'end_date': datetime(2025, 8, 22)
            },
            {
                'employer': 'Bridger Coal Company',
                'title': 'Electrical Apprenticeship Program',
                'opportunity_type': 'apprenticeship',
                'description': '''Launch your career with our comprehensive 4-year electrical apprenticeship program. This is a paid apprenticeship combining on-the-job training with classroom instruction.

You'll learn:
• Industrial electrical systems and motor controls
• Mining equipment electrical maintenance
• PLCs and automation systems
• High-voltage safety and arc flash protection
• Preventive maintenance scheduling

Our apprentices work on everything from conveyor systems to massive mining equipment. Upon completion, you'll be a journeyman electrician with specialized mining industry experience.

Partnership with IBEW Local 322 provides additional training opportunities and certification pathways.''',
                'requirements': '''• High school diploma or equivalent
• ODYC Electrical pathway participation preferred
• Basic math and mechanical aptitude
• Willingness to work underground and in all weather
• Pass comprehensive background check and physical
• Valid driver's license
• Commitment to 4-year program completion''',
                'pathway': 'Electrical & Instrumentation Technician',
                'duration': '4 years',
                'compensation': 'Starting $22/hour, increasing to $38/hour',
                'positions_available': 3,
                'application_deadline': datetime.now() + timedelta(days=60),
                'start_date': datetime(2025, 9, 1),
                'end_date': datetime(2029, 9, 1)
            },
            {
                'employer': 'Sweetwater Memorial Hospital',
                'title': 'Facilities Maintenance Technician',
                'opportunity_type': 'entry_level',
                'description': '''Join our facilities team maintaining critical healthcare infrastructure. You'll ensure our medical equipment, HVAC systems, and building operations run smoothly to support patient care.

Responsibilities include:
• Preventive maintenance on medical equipment
• HVAC system monitoring and basic repairs
• Plumbing and electrical troubleshooting
• Emergency generator testing and maintenance
• Work order management and documentation

This role offers stability in healthcare with opportunities to specialize in biomedical equipment or building automation systems. We provide extensive on-the-job training and professional development.''',
                'requirements': '''• ODYC Mechanical Maintenance pathway completion preferred
• Basic mechanical and electrical knowledge
• Ability to lift 50 lbs and work in confined spaces
• Excellent attention to detail for safety compliance
• Professional communication skills for hospital environment
• Willingness to be on-call for emergencies''',
                'pathway': 'Mechanical Maintenance Technician',
                'duration': 'Permanent position',
                'compensation': '$48,000-$58,000 annually',
                'positions_available': 2,
                'application_deadline': datetime.now() + timedelta(days=30),
                'start_date': datetime.now() + timedelta(days=45),
                'end_date': None
            },
            {
                'employer': 'Wyoming Machine Works',
                'title': 'Manufacturing Internship Program',
                'opportunity_type': 'internship',
                'description': '''Experience precision manufacturing in our state-of-the-art facility. This internship exposes you to advanced machining, welding, and assembly operations supporting regional industries.

You'll rotate through:
• CNC machining and programming
• Manual machining operations
• Welding and fabrication
• Quality control and inspection
• Project management and customer relations

Our internship provides exposure to lean manufacturing principles and Industry 4.0 technologies. Many interns continue as full-time machinists or technicians.''',
                'requirements': '''• Strong mechanical aptitude and interest in manufacturing
• Basic math skills and blueprint reading ability
• Safety-conscious mindset and attention to detail
• Physical ability to stand for extended periods
• Willingness to learn multiple manufacturing processes
• ODYC Mechanical pathway participation preferred''',
                'pathway': 'Mechanical Maintenance Technician',
                'duration': '16 weeks part-time during school year',
                'compensation': '$16/hour',
                'positions_available': 3,
                'application_deadline': datetime.now() + timedelta(days=21),
                'start_date': datetime(2025, 1, 15),
                'end_date': datetime(2025, 5, 15)
            }
        ]
        
        for opp_data in opportunities_data:
            # Find the employer
            employer = next((e for e in created_employers if e.company_name == opp_data['employer']), None)
            if not employer:
                continue
                
            # Find the pathway
            pathway = None
            if opp_data.get('pathway'):
                pathway = CareerPathway.query.filter_by(name=opp_data['pathway']).first()
            
            opportunity = EmployerOpportunity(
                employer_id=employer.id,
                title=opp_data['title'],
                opportunity_type=opp_data['opportunity_type'],
                description=opp_data['description'],
                requirements=opp_data['requirements'],
                pathway_id=pathway.id if pathway else None,
                duration=opp_data['duration'],
                compensation=opp_data['compensation'],
                positions_available=opp_data['positions_available'],
                application_deadline=opp_data['application_deadline'],
                start_date=opp_data['start_date'],
                end_date=opp_data['end_date']
            )
            db.session.add(opportunity)
            print(f"  ✅ Created opportunity: {opp_data['title']}")
        
        # Create sample sponsorships
        sponsorships_data = [
            {
                'employer': 'Genesis Alkali',
                'tier': 'gold',
                'annual_amount': 15000,
                'status': 'active',
                'pathway_focus': 'Process Operator',
                'benefits': {
                    'dashboard_access': True,
                    'early_talent_access': True,
                    'branding_enabled': True,
                    'curriculum_input': True
                }
            },
            {
                'employer': 'Bridger Coal Company',
                'tier': 'platinum',
                'annual_amount': 25000,
                'status': 'active',
                'pathway_focus': 'Electrical & Instrumentation Technician',
                'benefits': {
                    'dashboard_access': True,
                    'early_talent_access': True,
                    'branding_enabled': True,
                    'curriculum_input': True,
                    'exclusive_events': True,
                    'candidate_matching': True
                }
            }
        ]
        
        for sponsor_data in sponsorships_data:
            employer = next((e for e in created_employers if e.company_name == sponsor_data['employer']), None)
            if not employer:
                continue
                
            pathway = CareerPathway.query.filter_by(name=sponsor_data['pathway_focus']).first()
            
            sponsorship = Sponsorship(
                employer_id=employer.id,
                tier=sponsor_data['tier'],
                annual_amount=sponsor_data['annual_amount'],
                status=sponsor_data['status'],
                pathway_focus_id=pathway.id if pathway else None,
                billing_contact=employer.contact_name,
                billing_email=employer.contact_email,
                **sponsor_data['benefits']
            )
            db.session.add(sponsorship)
            print(f"  ✅ Created {sponsor_data['tier']} sponsorship: {sponsor_data['employer']}")
        
        db.session.commit()
        print(f"\n🎉 Successfully seeded employer portal with {len(created_employers)} employers and sample opportunities!")
        print("\n📧 Employer Login Credentials:")
        for employer_data in employers_data:
            print(f"  • {employer_data['user']['email']} / password123")

if __name__ == '__main__':
    seed_employer_data()