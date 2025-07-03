#!/usr/bin/env python3
"""
Industry and Career Pathway seeder for ODYC
Creates Southwest Wyoming industry data, job roles, and career pathways
"""

from app import app, db
from models import (Industry, JobRole, CareerPathway, EmployerPartner, 
                   PathwayModule, CurriculumModule)

def create_industry_data():
    with app.app_context():
        print("Creating Southwest Wyoming industry and career pathway data...")
        
        # Create Industries
        industries_data = [
            {
                'name': 'Manufacturing',
                'description': 'Advanced manufacturing including chemical processing, equipment manufacturing, and industrial automation in Southwest Wyoming.',
                'region': 'Southwest Wyoming'
            },
            {
                'name': 'Energy & Mining',
                'description': 'Oil, gas, coal, and renewable energy production, along with supporting services and equipment.',
                'region': 'Southwest Wyoming'
            },
            {
                'name': 'Healthcare',
                'description': 'Regional healthcare services including hospitals, clinics, and specialized medical care.',
                'region': 'Southwest Wyoming'
            },
            {
                'name': 'Transportation & Logistics',
                'description': 'Rail, trucking, and logistics operations supporting regional and interstate commerce.',
                'region': 'Southwest Wyoming'
            },
            {
                'name': 'Construction & Trades',
                'description': 'Commercial and industrial construction, maintenance, and skilled trades supporting regional development.',
                'region': 'Southwest Wyoming'
            }
        ]
        
        created_industries = {}
        for industry_data in industries_data:
            existing = Industry.query.filter_by(name=industry_data['name']).first()
            if not existing:
                industry = Industry(
                    name=industry_data['name'],
                    description=industry_data['description'],
                    region=industry_data['region'],
                    is_active=True
                )
                db.session.add(industry)
                created_industries[industry_data['name']] = industry
                print(f"Created industry: {industry.name}")
            else:
                created_industries[industry_data['name']] = existing
        
        db.session.commit()
        
        # Create Job Roles
        job_roles_data = [
            {
                'title': 'Electrical & Instrumentation Technician',
                'industry': 'Manufacturing',
                'description': 'Install, maintain, and troubleshoot electrical systems and instrumentation in industrial facilities. Work with PLCs, control systems, and automation equipment.',
                'requirements': 'High school diploma, technical training in electrical systems, understanding of industrial control systems, ability to read electrical schematics',
                'salary_range': '$45,000 - $65,000',
                'growth_outlook': 'High',
                'local_demand': 25,
                'education_level': 'High School + Technical Training',
                'is_priority': True
            },
            {
                'title': 'Process Operator',
                'industry': 'Manufacturing',
                'description': 'Monitor and control manufacturing processes, operate equipment, ensure quality standards, and maintain safety protocols in chemical or manufacturing plants.',
                'requirements': 'High school diploma, mechanical aptitude, attention to detail, ability to work in team environment, willingness to work rotating shifts',
                'salary_range': '$40,000 - $58,000',
                'growth_outlook': 'High',
                'local_demand': 35,
                'education_level': 'High School',
                'is_priority': True
            },
            {
                'title': 'Maintenance Technician',
                'industry': 'Manufacturing',
                'description': 'Perform preventive and corrective maintenance on industrial equipment, troubleshoot mechanical and electrical problems, ensure optimal equipment performance.',
                'requirements': 'High school diploma, mechanical skills, basic electrical knowledge, experience with hand and power tools, problem-solving abilities',
                'salary_range': '$42,000 - $62,000',
                'growth_outlook': 'High',
                'local_demand': 20,
                'education_level': 'High School + Experience',
                'is_priority': True
            },
            {
                'title': 'Petroleum Production Technician',
                'industry': 'Energy & Mining',
                'description': 'Operate and maintain equipment for oil and gas extraction, monitor production systems, ensure compliance with safety and environmental regulations.',
                'requirements': 'High school diploma, mechanical aptitude, safety training, ability to work outdoors, physical fitness for field work',
                'salary_range': '$48,000 - $70,000',
                'growth_outlook': 'Medium',
                'local_demand': 30,
                'education_level': 'High School',
                'is_priority': True
            },
            {
                'title': 'Certified Nursing Assistant (CNA)',
                'industry': 'Healthcare',
                'description': 'Provide direct patient care under supervision, assist with daily living activities, monitor patient conditions, maintain patient records.',
                'requirements': 'High school diploma, CNA certification, compassionate nature, attention to detail, good communication skills',
                'salary_range': '$28,000 - $38,000',
                'growth_outlook': 'High',
                'local_demand': 15,
                'education_level': 'High School + Certification',
                'is_priority': False
            },
            {
                'title': 'Heavy Equipment Operator',
                'industry': 'Construction & Trades',
                'description': 'Operate heavy machinery for construction, mining, and infrastructure projects. Includes excavators, bulldozers, cranes, and other large equipment.',
                'requirements': 'High school diploma, equipment operation training, safety certification, good hand-eye coordination, attention to safety protocols',
                'salary_range': '$38,000 - $55,000',
                'growth_outlook': 'Medium',
                'local_demand': 18,
                'education_level': 'High School + Training',
                'is_priority': False
            },
            {
                'title': 'Logistics Coordinator',
                'industry': 'Transportation & Logistics',
                'description': 'Coordinate shipments, manage inventory, track deliveries, communicate with carriers and customers, ensure efficient supply chain operations.',
                'requirements': 'High school diploma, organizational skills, computer proficiency, communication skills, attention to detail',
                'salary_range': '$35,000 - $48,000',
                'growth_outlook': 'Medium',
                'local_demand': 12,
                'education_level': 'High School',
                'is_priority': False
            }
        ]
        
        created_job_roles = {}
        for job_data in job_roles_data:
            industry = created_industries[job_data['industry']]
            existing = JobRole.query.filter_by(title=job_data['title']).first()
            if not existing:
                job_role = JobRole(
                    title=job_data['title'],
                    industry_id=industry.id,
                    description=job_data['description'],
                    requirements=job_data['requirements'],
                    salary_range=job_data['salary_range'],
                    growth_outlook=job_data['growth_outlook'],
                    local_demand=job_data['local_demand'],
                    education_level=job_data['education_level'],
                    is_priority=job_data['is_priority']
                )
                db.session.add(job_role)
                created_job_roles[job_data['title']] = job_role
                print(f"Created job role: {job_role.title}")
            else:
                created_job_roles[job_data['title']] = existing
        
        db.session.commit()
        
        # Create Career Pathways
        pathways_data = [
            {
                'name': 'Manufacturing Technician Pathway',
                'job_role': 'Electrical & Instrumentation Technician',
                'description': 'Comprehensive pathway preparing students for high-demand electrical and instrumentation roles in Southwest Wyoming manufacturing facilities.',
                'duration_months': 18,
                'prerequisites': 'High school diploma, basic math skills, interest in technical fields',
                'career_outcomes': 'Entry-level technician position with potential advancement to senior technician, supervisor, or engineering support roles. Average starting salary $45,000.',
                'employer_partners': 'Local chemical plants, manufacturing facilities, and industrial automation companies'
            },
            {
                'name': 'Process Operations Pathway',
                'job_role': 'Process Operator',
                'description': 'Direct pathway to process operator roles in chemical manufacturing and industrial processing facilities in the region.',
                'duration_months': 12,
                'prerequisites': 'High school diploma, mechanical aptitude, ability to work shifts',
                'career_outcomes': 'Process operator position with advancement opportunities to senior operator, training coordinator, or plant supervisor. Strong job security in growing field.',
                'employer_partners': 'Regional chemical processing plants, manufacturing facilities'
            },
            {
                'name': 'Energy Production Pathway',
                'job_role': 'Petroleum Production Technician',
                'description': 'Pathway focused on oil and gas production operations, preparing students for careers in Southwest Wyoming energy sector.',
                'duration_months': 15,
                'prerequisites': 'High school diploma, physical fitness, interest in outdoor work',
                'career_outcomes': 'Production technician role with opportunities for advancement to senior technician, field supervisor, or operations management.',
                'employer_partners': 'Regional oil and gas companies, production service providers'
            },
            {
                'name': 'Industrial Maintenance Pathway',
                'job_role': 'Maintenance Technician',
                'description': 'Multi-skilled maintenance pathway covering mechanical, electrical, and troubleshooting skills for industrial environments.',
                'duration_months': 16,
                'prerequisites': 'High school diploma, mechanical aptitude, problem-solving skills',
                'career_outcomes': 'Maintenance technician position with advancement to lead technician, maintenance supervisor, or specialized technical roles.',
                'employer_partners': 'Manufacturing facilities, power plants, industrial complexes'
            }
        ]
        
        created_pathways = {}
        for pathway_data in pathways_data:
            job_role = created_job_roles[pathway_data['job_role']]
            existing = CareerPathway.query.filter_by(name=pathway_data['name']).first()
            if not existing:
                pathway = CareerPathway(
                    name=pathway_data['name'],
                    job_role_id=job_role.id,
                    description=pathway_data['description'],
                    duration_months=pathway_data['duration_months'],
                    prerequisites=pathway_data['prerequisites'],
                    career_outcomes=pathway_data['career_outcomes'],
                    employer_partners=pathway_data['employer_partners'],
                    is_active=True
                )
                db.session.add(pathway)
                created_pathways[pathway_data['name']] = pathway
                print(f"Created career pathway: {pathway.name}")
            else:
                created_pathways[pathway_data['name']] = existing
        
        db.session.commit()
        
        # Link curriculum modules to pathways
        print("Linking curriculum modules to career pathways...")
        
        # Get existing curriculum modules
        intro_module = CurriculumModule.query.filter_by(title='Introduction to Professional Development').first()
        industry_module = CurriculumModule.query.filter_by(title='Industry Knowledge and Market Trends').first()
        leadership_module = CurriculumModule.query.filter_by(title='Leadership and Team Management').first()
        digital_module = CurriculumModule.query.filter_by(title='Digital Skills and Technology Adaptation').first()
        
        if intro_module and industry_module and leadership_module and digital_module:
            # Link modules to pathways
            pathway_module_links = [
                # Manufacturing Technician Pathway
                {'pathway': 'Manufacturing Technician Pathway', 'module': intro_module, 'order': 1, 'required': True},
                {'pathway': 'Manufacturing Technician Pathway', 'module': industry_module, 'order': 2, 'required': True},
                {'pathway': 'Manufacturing Technician Pathway', 'module': digital_module, 'order': 3, 'required': True},
                {'pathway': 'Manufacturing Technician Pathway', 'module': leadership_module, 'order': 4, 'required': False},
                
                # Process Operations Pathway
                {'pathway': 'Process Operations Pathway', 'module': intro_module, 'order': 1, 'required': True},
                {'pathway': 'Process Operations Pathway', 'module': industry_module, 'order': 2, 'required': True},
                {'pathway': 'Process Operations Pathway', 'module': digital_module, 'order': 3, 'required': False},
                
                # Energy Production Pathway
                {'pathway': 'Energy Production Pathway', 'module': intro_module, 'order': 1, 'required': True},
                {'pathway': 'Energy Production Pathway', 'module': industry_module, 'order': 2, 'required': True},
                {'pathway': 'Energy Production Pathway', 'module': leadership_module, 'order': 3, 'required': False},
                
                # Industrial Maintenance Pathway
                {'pathway': 'Industrial Maintenance Pathway', 'module': intro_module, 'order': 1, 'required': True},
                {'pathway': 'Industrial Maintenance Pathway', 'module': digital_module, 'order': 2, 'required': True},
                {'pathway': 'Industrial Maintenance Pathway', 'module': industry_module, 'order': 3, 'required': True},
                {'pathway': 'Industrial Maintenance Pathway', 'module': leadership_module, 'order': 4, 'required': False}
            ]
            
            for link_data in pathway_module_links:
                pathway = created_pathways[link_data['pathway']]
                existing_link = PathwayModule.query.filter_by(
                    pathway_id=pathway.id,
                    module_id=link_data['module'].id
                ).first()
                
                if not existing_link:
                    pathway_module = PathwayModule(
                        pathway_id=pathway.id,
                        module_id=link_data['module'].id,
                        order_in_pathway=link_data['order'],
                        is_required=link_data['required'],
                        estimated_completion_weeks=link_data['module'].duration_weeks
                    )
                    db.session.add(pathway_module)
                    print(f"Linked {link_data['module'].title} to {pathway.name}")
        
        # Create Employer Partners
        employers_data = [
            {
                'company_name': 'Genesis Alkali',
                'industry': 'Manufacturing',
                'contact_name': 'HR Department',
                'contact_email': 'careers@genesisalkali.com',
                'address': 'Green River, WY',
                'employee_count': '201-500',
                'participation_level': 'Full Partner',
                'hiring_needs': 'Process operators, maintenance technicians, electrical technicians. Projected 15-20 new hires annually.',
                'mentors_provided': 3
            },
            {
                'company_name': 'Bridger Coal Company',
                'industry': 'Energy & Mining',
                'contact_name': 'Workforce Development',
                'address': 'Rock Springs, WY',
                'employee_count': '101-200',
                'participation_level': 'Hiring Partner',
                'hiring_needs': 'Heavy equipment operators, maintenance personnel, production technicians.',
                'mentors_provided': 2
            },
            {
                'company_name': 'Memorial Hospital of Sweetwater County',
                'industry': 'Healthcare',
                'contact_name': 'Human Resources',
                'address': 'Rock Springs, WY',
                'employee_count': '501-1000',
                'participation_level': 'Mentor Provider',
                'hiring_needs': 'CNAs, medical assistants, healthcare support roles.',
                'mentors_provided': 4
            }
        ]
        
        for employer_data in employers_data:
            industry = created_industries[employer_data['industry']]
            existing = EmployerPartner.query.filter_by(company_name=employer_data['company_name']).first()
            if not existing:
                employer = EmployerPartner(
                    company_name=employer_data['company_name'],
                    industry_id=industry.id,
                    contact_name=employer_data.get('contact_name'),
                    contact_email=employer_data.get('contact_email'),
                    address=employer_data.get('address'),
                    employee_count=employer_data['employee_count'],
                    participation_level=employer_data['participation_level'],
                    hiring_needs=employer_data['hiring_needs'],
                    mentors_provided=employer_data['mentors_provided'],
                    is_active=True
                )
                db.session.add(employer)
                print(f"Created employer partner: {employer.company_name}")
        
        db.session.commit()
        
        print(f"\nSouthwest Wyoming industry data creation completed!")
        print(f"Created:")
        print(f"- {len(created_industries)} industries")
        print(f"- {len(created_job_roles)} job roles")
        print(f"- {len(created_pathways)} career pathways")
        print(f"- 3 employer partners")
        
        print(f"\nPriority job roles (high local demand):")
        for role_name, role in created_job_roles.items():
            if role.is_priority:
                print(f"- {role.title}: {role.local_demand} projected openings")
        
        print(f"\nThe platform now supports:")
        print(f"- Industry-specific career pathways")
        print(f"- Job role targeting and workforce pipeline development")
        print(f"- Employer partner engagement and hiring needs tracking")
        print(f"- Student career interest tracking and personalized roadmaps")

if __name__ == '__main__':
    create_industry_data()