#!/usr/bin/env python3
"""
Career Roadmaps seeder for ODYC
Creates detailed, authentic career roadmaps based on WWCC and RSHS programs
"""

from app import app, db
from models import (CurriculumModule, CareerPathway, JobRole, Industry, 
                   PathwayModule)

def create_career_roadmaps():
    with app.app_context():
        print("Creating detailed career roadmaps based on WWCC and RSHS programs...")
        
        # Create detailed curriculum modules for each career pathway
        roadmap_modules = [
            # === ELECTRICAL & INSTRUMENTATION TECHNICIAN PATHWAY ===
            {
                'title': 'Foundation: Basic Electricity and Safety',
                'description': 'Essential electrical fundamentals and industrial safety protocols aligned with WWCC Electrical & Instrumentation Technology program.',
                'content': '''# Foundation: Basic Electricity and Safety

This module establishes the fundamental knowledge base for your journey as an Electrical & Instrumentation Technician, following Western Wyoming Community College's industry-partnered curriculum.

## Skill Milestone 1: Master DC/AC Circuit Fundamentals
**Target Grade Level:** 11th Grade (Dual Enrollment Available)

### Learning Objectives
- Understand Ohm's Law and its applications
- Calculate voltage, current, and resistance in series and parallel circuits
- Use digital multimeters and basic electrical test equipment
- Read and interpret basic electrical schematics

### Example Activities & Classes
**At Rock Springs High School:**
- Physics I with electrical circuits emphasis
- CTE Academy - Basic Electronics (dual enrollment prep)
- Participate in SkillsUSA Electronics competition

**Dual Enrollment at WWCC:**
- ELEC 1010: Basic Electricity DC (3 credits)
- ELEC 1020: Basic Electricity AC (3 credits)

### Milestone Assessment
- Successfully wire and troubleshoot basic AC/DC circuits
- Pass WWCC electrical fundamentals assessment
- Complete safety certification requirements

## Skill Milestone 2: Industrial Safety and OSHA-10 Certification
**Target Grade Level:** 11th-12th Grade

### Learning Objectives
- Complete OSHA-10 Hour General Industry certification
- Understand lockout/tagout (LOTO) procedures
- Identify electrical hazards and safety protocols
- Learn proper use of personal protective equipment (PPE)

### Example Activities & Classes
**Through RSHS CTE Academy:**
- Industrial Safety course (partnership with local employers)
- OSHA-10 certification workshop
- Safety presentations by Genesis Alkali safety managers

**Industry Connections:**
- Safety training sessions at local chemical plants
- Job shadowing with plant electrical departments
- Mentorship with certified safety professionals

### Milestone Assessment
- OSHA-10 General Industry certification
- Demonstrate proper LOTO procedures
- Complete workplace safety scenario assessments

## Professional Skills Development
Throughout this foundation phase:
- Professional communication in industrial settings
- Technical documentation and record keeping
- Team collaboration and problem-solving
- Introduction to continuous improvement mindset

## Pathway to Next Module
Students completing this foundation module will be prepared for advanced instrumentation and control systems training in Year 2 of the pathway.''',
                'learning_objectives': '''- Master fundamental electrical principles including Ohm's Law, AC/DC circuits, and basic electrical measurements
- Obtain OSHA-10 General Industry certification and demonstrate workplace safety protocols
- Read and interpret basic electrical schematics and wiring diagrams
- Use digital multimeters and basic electrical test equipment effectively
- Understand industrial electrical safety including lockout/tagout procedures''',
                'resources': '''**Required Textbooks:**
- "Electrical Motor Controls for Integrated Systems" by Gary Rockis & Glen Mazur
- OSHA 10-Hour General Industry Training materials

**Equipment & Tools:**
- Digital multimeter (Fluke 87V recommended)
- Basic electrical hand tools
- Circuit training boards
- Safety equipment (hard hat, safety glasses, electrical gloves)

**Industry Partnerships:**
- Genesis Alkali - Safety training and facility tours
- Local electrical contractors - Apprenticeship information
- IBEW Local 415 - Union apprenticeship opportunities

**Online Resources:**
- OSHA 10-Hour online training portal
- Mike Holt Enterprises electrical training videos
- WWCC online learning management system''',
                'assignments': '''**Week 1-2: Circuit Analysis Project**
1. Build and test 5 different AC/DC circuits
2. Calculate theoretical vs. actual measurements
3. Document findings in technical report format
4. Present results to mentor group

**Week 3-4: Safety Certification**
1. Complete OSHA-10 General Industry online training
2. Pass certification exam (minimum 80%)
3. Complete hands-on safety demonstration
4. Create workplace safety checklist for electrical work

**Capstone Project: Industrial Electrical Assessment**
1. Partner with local employer for real-world project
2. Assess electrical system in industrial setting
3. Create technical report with recommendations
4. Present findings to industry mentor and WWCC instructor''',
                'duration_weeks': 4,
                'difficulty_level': 'beginner',
                'order_index': 1
            },
            {
                'title': 'Instrumentation Fundamentals and Process Control',
                'description': 'Core instrumentation concepts and process control systems aligned with WWCC curriculum and local industry needs.',
                'content': '''# Instrumentation Fundamentals and Process Control

Building on electrical fundamentals, this module introduces students to industrial instrumentation and process control systems used throughout Southwest Wyoming's manufacturing and energy sectors.

## Skill Milestone 3: Understand Loop Diagrams and P&IDs
**Target Grade Level:** 12th Grade (WWCC Year 1)

### Learning Objectives
- Read and interpret Piping and Instrumentation Diagrams (P&IDs)
- Understand ISA (International Society of Automation) symbols and standards
- Trace signal flow through instrument loops
- Identify process variables: pressure, temperature, flow, level

### Example Activities & Classes
**At WWCC:**
- INEL 1500: Instrumentation I (4 credits)
- INEL 1510: Instrumentation II (4 credits)
- Process Control Fundamentals course

**Industry Connections:**
- Plant tours at Genesis Alkali process facilities
- Guest lectures from local process engineers
- Hands-on training with actual plant P&IDs

### Milestone Assessment
- Successfully interpret complex P&ID drawings
- Identify all major instrumentation symbols
- Trace complete control loops from sensor to final control element

## Skill Milestone 4: Calibrate Process Instruments
**Target Grade Level:** 12th Grade/WWCC Year 1

### Learning Objectives
- Calibrate pressure, temperature, and flow transmitters
- Use precision test equipment (calibrators, decade boxes)
- Understand measurement accuracy, precision, and uncertainty
- Document calibration procedures and results

### Example Activities & Classes
**WWCC Laboratory Work:**
- Hands-on calibration of Rosemount transmitters
- Use of Fluke calibrators and test equipment
- Real-world instrument maintenance procedures
- Quality control and documentation practices

**Industry Training:**
- Mentorship with Genesis Alkali instrument technicians
- Participate in scheduled plant maintenance activities
- Learn plant-specific calibration procedures

### Milestone Assessment
- Calibrate instruments to within specified tolerances
- Complete calibration documentation per industry standards
- Demonstrate troubleshooting of out-of-specification instruments

## Advanced Topics
### Control System Basics
- Introduction to PLC (Programmable Logic Controller) systems
- HMI (Human Machine Interface) operation
- DCS (Distributed Control System) overview
- Safety instrumented systems (SIS)

### Communication Protocols
- 4-20mA current loops
- HART communication protocol
- Foundation Fieldbus basics
- Ethernet/IP industrial networks

## Pathway to Next Module
Successful completion prepares students for advanced electrical systems and National Electrical Code training in their final preparation phase.''',
                'learning_objectives': '''- Read and interpret P&ID drawings and ISA instrumentation symbols
- Calibrate process instruments including pressure, temperature, and flow transmitters
- Understand process control loops and signal flow from sensor to final control element
- Use precision test equipment for instrument calibration and troubleshooting
- Document instrument maintenance and calibration per industry standards''',
                'resources': '''**Technical References:**
- "Instrument Engineers' Handbook" by Béla Lipták
- ISA-5.1 Instrumentation Symbols and Identification Standard
- Plant-specific P&ID drawings from local facilities

**Laboratory Equipment:**
- Fluke 754 Process Calibrator
- Rosemount pressure and temperature transmitters
- Process training simulators
- PLC training systems (Allen-Bradley MicroLogix)

**Industry Resources:**
- Genesis Alkali process documentation
- Local utility plant instrumentation systems
- Mining equipment instrumentation examples

**Professional Development:**
- ISA (International Society of Automation) membership
- Local ISA section meetings and technical presentations
- Instrument technician certification preparation materials''',
                'assignments': '''**Project 1: P&ID Analysis**
1. Analyze complete P&ID from local industrial facility
2. Identify all instrumentation and control loops
3. Create presentation explaining process flow
4. Quiz mentor group on key control strategies

**Project 2: Instrument Calibration Lab**
1. Calibrate 3 different types of process transmitters
2. Document procedures using industry-standard forms
3. Troubleshoot intentionally miscalibrated instruments
4. Present findings to industry mentor

**Capstone: Control Loop Documentation**
1. Work with industry partner to document actual control loop
2. Create as-built P&ID drawing
3. Develop calibration procedure for all loop instruments
4. Present to plant engineering team''',
                'duration_weeks': 6,
                'difficulty_level': 'intermediate',
                'order_index': 2
            },
            
            # === PROCESS OPERATOR PATHWAY ===
            {
                'title': 'Process Operations and Safety Systems',
                'description': 'Foundation training for process operators in chemical manufacturing and industrial processing, based on regional employer needs.',
                'content': '''# Process Operations and Safety Systems

This module prepares students for entry-level process operator positions in Southwest Wyoming's chemical manufacturing and industrial processing facilities, with direct input from Genesis Alkali and other regional employers.

## Skill Milestone 1: Master Basic Process Operations
**Target Grade Level:** 11th-12th Grade

### Learning Objectives
- Understand unit operations in chemical processing
- Monitor and control process variables
- Respond to process alarms and upsets
- Maintain process safety and environmental compliance

### Example Activities & Classes
**At RSHS CTE Academy:**
- Chemistry II with industrial applications focus
- Environmental Science with process safety emphasis
- Manufacturing processes course (dual enrollment prep)

**Dual Enrollment at WWCC:**
- CHEM 1020: General Chemistry I with lab
- Plant Operations fundamentals course
- Process Safety Management overview

**Industry Connections:**
- Job shadowing with Genesis Alkali operators
- Tour of regional chemical processing facilities
- Guest lectures from experienced process operators

### Milestone Assessment
- Demonstrate understanding of material and energy balances
- Successfully operate process simulation software
- Complete plant emergency response scenarios

## Skill Milestone 2: Complete Hazmat and Emergency Response Training
**Target Grade Level:** 12th Grade

### Learning Objectives
- Understand chemical hazards and material safety data sheets (SDS)
- Respond to chemical spills and emergency situations
- Use personal protective equipment appropriately
- Implement emergency shutdown procedures

### Example Activities & Classes
**Specialized Training:**
- Hazmat Awareness and Operations certification
- First Aid/CPR certification
- Confined space entry awareness
- Emergency response team training

**Industry Training:**
- Participation in plant emergency drills
- Training with local fire department hazmat team
- OSHA 30-Hour Process Safety Management

### Milestone Assessment
- Hazmat Operations certification
- Demonstrate emergency response procedures
- Pass comprehensive safety knowledge exam

## Advanced Process Concepts
### Quality Control
- Statistical process control (SPC)
- Quality testing procedures
- Documentation and record keeping
- Continuous improvement methodologies

### Environmental Compliance
- Air emissions monitoring
- Water treatment and discharge
- Waste management procedures
- Environmental reporting requirements

## Pathway to Next Module
Students advance to advanced process control and team leadership training.''',
                'learning_objectives': '''- Understand fundamental unit operations in chemical processing including distillation, reaction, and separation
- Monitor and control process variables using distributed control systems (DCS)
- Respond effectively to process alarms, upsets, and emergency situations
- Complete Hazmat Operations certification and emergency response training
- Demonstrate environmental compliance and safety management procedures''',
                'resources': '''**Industry Training Materials:**
- Genesis Alkali operator training manuals
- Chemical processing fundamentals textbooks
- OSHA Process Safety Management guidelines
- Emergency response procedures from local facilities

**Simulation Software:**
- HYSYS process simulation training
- DCS operator training simulators
- Emergency response scenario software

**Certifications:**
- Hazmat Awareness and Operations
- OSHA 30-Hour Process Safety Management
- First Aid/CPR certification
- Confined space entry awareness

**Professional Development:**
- American Institute of Chemical Engineers (AIChE) student membership
- Local safety council participation
- Process operator certification study materials''',
                'assignments': '''**Week 1-2: Process Flow Analysis**
1. Analyze material and energy balance for chemical process
2. Create process flow diagram for assigned unit operation
3. Calculate theoretical yields and efficiency
4. Present findings to industry mentor

**Week 3-4: Emergency Response Simulation**
1. Participate in plant emergency response drill
2. Document response procedures and timing
3. Identify areas for improvement
4. Create emergency response checklist

**Capstone: Operator Training Manual**
1. Partner with local facility to create training module
2. Develop step-by-step operating procedures
3. Include safety considerations and emergency procedures
4. Present to plant management and training department''',
                'duration_weeks': 5,
                'difficulty_level': 'intermediate',
                'order_index': 1
            },
            
            # === MECHANICAL MAINTENANCE TECHNICIAN PATHWAY ===
            {
                'title': 'Mechanical Systems and Maintenance Fundamentals',
                'description': 'Comprehensive mechanical maintenance training aligned with WWCC Industrial Maintenance program and regional industry needs.',
                'content': '''# Mechanical Systems and Maintenance Fundamentals

This module provides comprehensive training in mechanical maintenance for industrial facilities, incorporating Western Wyoming Community College's industry-partnered curriculum developed with local mining, energy, and manufacturing employers.

## Skill Milestone 1: Master Preventive Maintenance Planning
**Target Grade Level:** 11th-12th Grade

### Learning Objectives
- Develop and implement preventive maintenance schedules
- Use computerized maintenance management systems (CMMS)
- Plan and organize maintenance work orders
- Understand reliability-centered maintenance (RCM) principles

### Example Activities & Classes
**At RSHS CTE Academy:**
- Industrial Technology course
- Computer-aided drafting (CAD) with mechanical focus
- Project management fundamentals

**Dual Enrollment at WWCC:**
- Industrial Maintenance certificate courses
- Mechanical systems fundamentals
- Maintenance planning and scheduling

**Industry Connections:**
- Job shadowing with Bridger Coal maintenance teams
- Plant maintenance tours at local facilities
- Mentorship with experienced maintenance supervisors

### Milestone Assessment
- Create comprehensive preventive maintenance program
- Demonstrate CMMS software proficiency
- Present maintenance planning project to industry panel

## Skill Milestone 2: Troubleshoot Hydraulic and Pneumatic Systems
**Target Grade Level:** 12th Grade/WWCC Year 1

### Learning Objectives
- Understand hydraulic and pneumatic system principles
- Read and interpret fluid power schematics
- Troubleshoot system malfunctions and failures
- Replace and repair hydraulic and pneumatic components

### Example Activities & Classes
**WWCC Laboratory Training:**
- Hands-on hydraulic system troubleshooting
- Pneumatic circuit design and testing
- Industrial equipment maintenance procedures
- System diagnostics and repair techniques

**Specialized Certifications:**
- WWCC Industrial Maintenance Mechanics-Hydraulics Certificate
- Fluid power troubleshooting certification
- Mobile hydraulics training for mining equipment

### Milestone Assessment
- Successfully diagnose and repair hydraulic system failures
- Design and build pneumatic control circuits
- Complete industry-standard troubleshooting scenarios

## Advanced Maintenance Topics
### Mechanical Drive Systems
- Belt and chain drive maintenance
- Gear reducer service and repair
- Coupling alignment and installation
- Bearing analysis and replacement

### Rotating Equipment
- Pump maintenance and repair
- Motor alignment and balancing
- Vibration analysis fundamentals
- Predictive maintenance techniques

### Welding and Fabrication
- Basic arc welding for maintenance applications
- Cutting and torch operations
- Fabrication of replacement parts
- Welding safety and certification

## Pathway to Next Module
Advanced training in predictive maintenance technologies and leadership development for senior technician roles.''',
                'learning_objectives': '''- Develop and implement comprehensive preventive maintenance programs using CMMS software
- Troubleshoot and repair hydraulic and pneumatic systems in industrial applications
- Read and interpret mechanical drawings, schematics, and technical documentation
- Perform precision alignment, balancing, and installation of rotating equipment
- Complete welding and fabrication tasks for maintenance and repair applications''',
                'resources': '''**Technical References:**
- "Maintenance Planning and Scheduling Handbook" by Don Nyman
- Hydraulics and pneumatics training manuals
- Industrial equipment manufacturer service manuals
- WWCC Industrial Maintenance program materials

**Training Equipment:**
- Hydraulic training systems with fault simulation
- Pneumatic training panels and components
- Precision measurement and alignment tools
- Welding equipment and safety gear

**Industry Resources:**
- Local mining equipment maintenance procedures
- Power plant maintenance documentation
- Chemical facility mechanical systems
- Construction equipment service manuals

**Certifications Available:**
- WWCC Industrial Maintenance certificates
- AWS welding certifications
- Fluid power troubleshooting certification
- Vibration analysis Level I training''',
                'assignments': '''**Project 1: Maintenance Program Development**
1. Partner with local facility to assess current maintenance practices
2. Develop improved preventive maintenance schedule
3. Calculate potential cost savings and reliability improvements
4. Present recommendations to facility management

**Project 2: Hydraulic System Diagnosis**
1. Troubleshoot complex hydraulic system failure
2. Document diagnostic procedures and findings
3. Recommend repair solutions with cost analysis
4. Implement repairs and verify system performance

**Capstone: Equipment Overhaul Project**
1. Complete major overhaul of industrial equipment
2. Document all procedures with photos and measurements
3. Create maintenance manual for future reference
4. Train other students on maintenance procedures''',
                'duration_weeks': 6,
                'difficulty_level': 'intermediate',
                'order_index': 1
            }
        ]
        
        # Create the curriculum modules
        created_modules = []
        for module_data in roadmap_modules:
            existing_module = CurriculumModule.query.filter_by(title=module_data['title']).first()
            if not existing_module:
                module = CurriculumModule(
                    title=module_data['title'],
                    description=module_data['description'],
                    content=module_data['content'],
                    learning_objectives=module_data['learning_objectives'],
                    resources=module_data['resources'],
                    assignments=module_data['assignments'],
                    duration_weeks=module_data['duration_weeks'],
                    difficulty_level=module_data['difficulty_level'],
                    order_index=module_data['order_index'],
                    is_active=True
                )
                db.session.add(module)
                created_modules.append(module)
                print(f"Created detailed roadmap module: {module.title}")
        
        db.session.commit()
        
        # Link the new modules to existing career pathways
        print("Linking detailed modules to career pathways...")
        
        # Get career pathways
        electrical_pathway = CareerPathway.query.filter_by(name='Manufacturing Technician Pathway').first()
        process_pathway = CareerPathway.query.filter_by(name='Process Operations Pathway').first()
        maintenance_pathway = CareerPathway.query.filter_by(name='Industrial Maintenance Pathway').first()
        
        # Get the new detailed modules
        electrical_modules = [
            CurriculumModule.query.filter_by(title='Foundation: Basic Electricity and Safety').first(),
            CurriculumModule.query.filter_by(title='Instrumentation Fundamentals and Process Control').first()
        ]
        
        process_modules = [
            CurriculumModule.query.filter_by(title='Process Operations and Safety Systems').first()
        ]
        
        maintenance_modules = [
            CurriculumModule.query.filter_by(title='Mechanical Systems and Maintenance Fundamentals').first()
        ]
        
        # Link modules to pathways
        pathway_links = []
        
        if electrical_pathway:
            for i, module in enumerate(electrical_modules, 1):
                if module:
                    existing_link = PathwayModule.query.filter_by(
                        pathway_id=electrical_pathway.id,
                        module_id=module.id
                    ).first()
                    
                    if not existing_link:
                        pathway_module = PathwayModule(
                            pathway_id=electrical_pathway.id,
                            module_id=module.id,
                            order_in_pathway=i + 10,  # Place after existing modules
                            is_required=True,
                            estimated_completion_weeks=module.duration_weeks
                        )
                        db.session.add(pathway_module)
                        pathway_links.append(f"{module.title} → {electrical_pathway.name}")
        
        if process_pathway:
            for i, module in enumerate(process_modules, 1):
                if module:
                    existing_link = PathwayModule.query.filter_by(
                        pathway_id=process_pathway.id,
                        module_id=module.id
                    ).first()
                    
                    if not existing_link:
                        pathway_module = PathwayModule(
                            pathway_id=process_pathway.id,
                            module_id=module.id,
                            order_in_pathway=i + 10,
                            is_required=True,
                            estimated_completion_weeks=module.duration_weeks
                        )
                        db.session.add(pathway_module)
                        pathway_links.append(f"{module.title} → {process_pathway.name}")
        
        if maintenance_pathway:
            for i, module in enumerate(maintenance_modules, 1):
                if module:
                    existing_link = PathwayModule.query.filter_by(
                        pathway_id=maintenance_pathway.id,
                        module_id=module.id
                    ).first()
                    
                    if not existing_link:
                        pathway_module = PathwayModule(
                            pathway_id=maintenance_pathway.id,
                            module_id=module.id,
                            order_in_pathway=i + 10,
                            is_required=True,
                            estimated_completion_weeks=module.duration_weeks
                        )
                        db.session.add(pathway_module)
                        pathway_links.append(f"{module.title} → {maintenance_pathway.name}")
        
        db.session.commit()
        
        print(f"\nDetailed career roadmaps creation completed!")
        print(f"Created {len(created_modules)} detailed pathway modules:")
        for module in created_modules:
            print(f"- {module.title} ({module.duration_weeks} weeks, {module.difficulty_level})")
        
        print(f"\nLinked {len(pathway_links)} modules to pathways:")
        for link in pathway_links:
            print(f"- {link}")
        
        print(f"\nRoadmaps now include:")
        print(f"✓ Authentic WWCC course alignments and dual enrollment options")
        print(f"✓ Specific skill milestones tied to industry certifications")
        print(f"✓ Real employer partnerships (Genesis Alkali, Bridger Coal, etc.)")
        print(f"✓ Grade-level progression from RSHS through WWCC programs")
        print(f"✓ Hands-on projects with local industry mentors")
        print(f"✓ Industry-recognized certifications (OSHA, Hazmat, ISA, etc.)")

if __name__ == '__main__':
    create_career_roadmaps()