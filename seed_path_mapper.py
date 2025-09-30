"""Seed database with real Simplot job and WWCC Industrial Maintenance program"""
import json
from app import app, db
from models import JobPosting, EducationProgram, SkillAlignment
from datetime import datetime

def seed_path_mapper():
    with app.app_context():
        print("🌱 Seeding Path Mapper data...")
        
        # Clear existing data
        SkillAlignment.query.delete()
        JobPosting.query.delete()
        EducationProgram.query.delete()
        db.session.commit()
        
        # 1. Create Simplot Industrial Maintenance Mechanic Job
        simplot_job = JobPosting(
            title="Industrial Maintenance Mechanic",
            employer="J.R. Simplot Company",
            location="Rock Springs, WY",
            url="https://careers.simplot.com/job/Rock-Springs-Industrial-Maintenance-Mechanic-%28Rock-Springs%2C-WY%29-WY-82901-8810/1328391600/",
            description="""The Mechanic works independently and with other plant personnel to perform preventative, predictive and routine maintenance tasks. This role includes troubleshooting issues, repairing failures of production and facilities equipment, and ensuring maximum equipment efficiency and effectiveness.""",
            required_skills=json.dumps([
                "Hydraulics",
                "Pneumatics",
                "Pump/Valve Repair & Rebuild",
                "Mechanical Alignment",
                "Blueprint Reading",
                "Repair Documentation",
                "Troubleshooting",
                "Mechanical/Millwright Duties"
            ]),
            education_requirements="High School Diploma or GED",
            experience_requirements="3+ years of related experience and/or training",
            physical_requirements="Lift and move heavy equipment; Climb ladders and work in high, precarious places; May be exposed to temperatures as low as -5 degrees",
            special_requirements="Aptitude test required prior to interview",
            is_active=True,
            posted_date=datetime.utcnow()
        )
        db.session.add(simplot_job)
        
        # 2. Create WWCC Industrial Maintenance Technology Program
        wwcc_program = EducationProgram(
            provider="Western Wyoming Community College (WWCC)",
            name="Industrial Maintenance Technology",
            program_type="A.A.S. & Certificate",
            url="https://www.westernwyoming.edu/academics/major-programs/manufacturing-industry/industrial-maintenance/",
            description="Industrial Maintenance Technicians—also known as Industrial Machinery Mechanics—are highly skilled professionals who keep essential equipment running in industries like power generation, manufacturing, mining, oil and gas, and wind energy.",
            learning_outcomes=json.dumps([
                "Plant safety & industrial rigging",
                "Blueprint reading",
                "Bearings, lubrication & centrifugal pumps",
                "Mechanical drives, piping systems & alignment",
                "Hydraulics & pneumatics",
                "Industrial electricity & motor controls",
                "Vibration analysis & troubleshooting",
                "Machining & welding"
            ]),
            duration_terms=4,  # ~2 years for AAS
            total_credits=60,  # Typical AAS credit count
            application_url="https://www.westernwyoming.edu/admissions-and-aid/apply-to-western/",
            advising_url="https://www.westernwyoming.edu/academics/support-services/academic-advising/",
            schedule_url="https://www.westernwyoming.edu/academics/class-schedule.php",
            financial_aid_url="https://www.westernwyoming.edu/admissions-and-aid/financial-aid/"
        )
        db.session.add(wwcc_program)
        db.session.commit()
        
        # 3. Create Skill Alignments (mapping job requirements to program outcomes)
        alignments = [
            {
                "job_skill": "Hydraulics",
                "program_outcome": "Hydraulics & pneumatics",
                "coverage_level": "covered",
                "notes": "Direct match - WWCC teaches hydraulic systems theory and application"
            },
            {
                "job_skill": "Pneumatics",
                "program_outcome": "Hydraulics & pneumatics",
                "coverage_level": "covered",
                "notes": "Direct match - WWCC teaches pneumatic systems theory and application"
            },
            {
                "job_skill": "Pump/Valve Repair & Rebuild",
                "program_outcome": "Bearings, lubrication & centrifugal pumps",
                "coverage_level": "covered",
                "notes": "Direct match - WWCC covers centrifugal pumps and valve maintenance"
            },
            {
                "job_skill": "Mechanical Alignment",
                "program_outcome": "Mechanical drives, piping systems & alignment",
                "coverage_level": "covered",
                "notes": "Direct match - WWCC teaches precision alignment techniques"
            },
            {
                "job_skill": "Blueprint Reading",
                "program_outcome": "Blueprint reading",
                "coverage_level": "covered",
                "notes": "Direct match - WWCC teaches technical drawing interpretation"
            },
            {
                "job_skill": "Repair Documentation",
                "program_outcome": "Vibration analysis & troubleshooting",
                "coverage_level": "partial",
                "notes": "WWCC teaches systematic troubleshooting and maintenance documentation"
            },
            {
                "job_skill": "Troubleshooting",
                "program_outcome": "Vibration analysis & troubleshooting",
                "coverage_level": "covered",
                "notes": "WWCC teaches systematic diagnostic approaches for equipment issues"
            },
            {
                "job_skill": "Mechanical/Millwright Duties",
                "program_outcome": "Machining & welding",
                "coverage_level": "covered",
                "notes": "WWCC provides hands-on training in machining, welding, and mechanical assembly"
            }
        ]
        
        for alignment_data in alignments:
            alignment = SkillAlignment(
                job_id=simplot_job.id,
                program_id=wwcc_program.id,
                **alignment_data
            )
            db.session.add(alignment)
        
        db.session.commit()
        
        print(f"✅ Created job: {simplot_job.title} at {simplot_job.employer}")
        print(f"✅ Created program: {wwcc_program.name} at {wwcc_program.provider}")
        print(f"✅ Created {len(alignments)} skill alignments")
        print("\n🎯 Path Mapper database seeded successfully!")
        print(f"\n📊 Coverage: {len([a for a in alignments if a['coverage_level'] == 'covered'])}/8 skills fully covered")

if __name__ == '__main__':
    seed_path_mapper()
