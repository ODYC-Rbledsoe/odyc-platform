#!/usr/bin/env python3
"""
Sample curriculum seeder for the Mentorship Platform
Creates demo curriculum modules for testing and demonstration
"""

from app import app, db
from models import CurriculumModule

def create_sample_curriculum():
    with app.app_context():
        print("Creating sample curriculum modules...")
        
        modules_data = [
            {
                'title': 'Introduction to Professional Development',
                'description': 'Foundation module covering personal branding, goal setting, and professional communication skills.',
                'content': '''# Introduction to Professional Development

Welcome to the first module of our mentorship curriculum! This module will help you establish a strong foundation for your professional journey.

## What You'll Learn
- How to create a professional personal brand
- Effective goal-setting strategies (SMART goals)
- Professional communication in workplace settings
- Network building fundamentals
- Time management and productivity techniques

## Key Topics

### 1. Personal Branding
Your personal brand is how you present yourself professionally. It includes:
- Your unique value proposition
- Professional online presence (LinkedIn, portfolio)
- Consistent messaging across platforms
- Building credibility and trust

### 2. Goal Setting
Learn to set and achieve meaningful career goals:
- SMART goals framework (Specific, Measurable, Achievable, Relevant, Time-bound)
- Breaking down long-term goals into actionable steps
- Tracking progress and adjusting strategies
- Celebrating milestones

### 3. Professional Communication
Master the art of workplace communication:
- Email etiquette and best practices
- Effective meeting participation
- Presentation skills
- Giving and receiving feedback

### 4. Networking
Build meaningful professional relationships:
- Identifying networking opportunities
- Conversation starters and follow-up strategies
- Using social media for professional networking
- Maintaining long-term relationships

## Action Items
By the end of this module, you should:
- Complete your professional profile assessment
- Set 3 SMART goals for the next 6 months
- Update your LinkedIn profile
- Identify 5 professionals you'd like to connect with''',
                'learning_objectives': '''- Understand the importance of personal branding in career development
- Apply SMART goal-setting framework to personal career objectives
- Demonstrate professional communication skills in various contexts
- Build a foundational professional network
- Develop effective time management strategies''',
                'resources': '''**Books:**
- "7 Habits of Highly Effective People" by Stephen Covey
- "How to Win Friends and Influence People" by Dale Carnegie

**Online Resources:**
- LinkedIn Learning: Professional Branding courses
- TED Talks: Career Development playlist
- Harvard Business Review: Communication articles

**Tools:**
- LinkedIn Profile optimization checklist
- Goal tracking templates
- Time management apps (Todoist, Trello)''',
                'assignments': '''**Week 1 Assignment: Personal Brand Audit**
1. Complete the personal brand assessment worksheet
2. Update your LinkedIn profile with new insights
3. Write a 250-word professional bio

**Week 2 Assignment: Goal Setting**
1. Set 3 SMART goals for your career development
2. Create action plans for each goal
3. Identify potential obstacles and solutions

**Final Project:**
Prepare a 5-minute presentation on your professional development plan, including your personal brand statement and key goals.''',
                'duration_weeks': 2,
                'difficulty_level': 'beginner',
                'order_index': 1
            },
            {
                'title': 'Industry Knowledge and Market Trends',
                'description': 'Deep dive into your chosen industry, understanding market dynamics, key players, and emerging trends.',
                'content': '''# Industry Knowledge and Market Trends

Understanding your industry landscape is crucial for career success. This module will help you become an informed professional who can contribute meaningfully to discussions and make strategic decisions.

## Learning Framework

### 1. Industry Analysis
- Market size and growth potential
- Key players and competitive landscape
- Value chain and business models
- Regulatory environment and compliance requirements

### 2. Trend Identification
- Technology disruptions and innovations
- Consumer behavior shifts
- Economic factors affecting the industry
- Global vs. local market considerations

### 3. Professional Positioning
- Where you fit in the industry ecosystem
- Skills most valued in your field
- Career paths and growth opportunities
- Thought leadership development

## Research Methods

### Primary Research
- Informational interviews with industry professionals
- Attending industry conferences and events
- Participating in professional associations
- Conducting surveys or focus groups

### Secondary Research
- Industry reports and white papers
- Financial statements and annual reports
- Trade publications and news sources
- Academic research and case studies

## Staying Current

### Daily Habits
- Read industry news (15-20 minutes daily)
- Follow thought leaders on social media
- Subscribe to relevant newsletters and podcasts
- Join industry discussion forums

### Weekly Activities
- Attend webinars or virtual events
- Read in-depth articles or reports
- Network with industry peers
- Update your knowledge tracker

### Monthly Goals
- Attend one industry event
- Complete one informational interview
- Read one industry book or major report
- Share insights on your professional platform''',
                'learning_objectives': '''- Analyze industry structure, key players, and competitive dynamics
- Identify and evaluate emerging trends affecting your field
- Develop systematic approach to staying current with industry developments
- Position yourself strategically within the industry landscape
- Create actionable insights from industry research''',
                'resources': '''**Industry Research Platforms:**
- IBISWorld - Industry reports and market research
- Statista - Market data and consumer insights
- PwC, McKinsey, Deloitte - Consulting reports
- Company annual reports and investor presentations

**News and Analysis:**
- Industry-specific trade publications
- Wall Street Journal, Financial Times
- Harvard Business Review
- MIT Technology Review

**Professional Networks:**
- Industry associations and professional groups
- LinkedIn industry groups
- Meetup professional events
- Industry conferences and trade shows''',
                'assignments': '''**Week 1: Industry Landscape Mapping**
1. Create a comprehensive industry map including major players, market segments, and value chain
2. Identify top 5 trends affecting your industry
3. Write a 500-word industry overview

**Week 2: Competitive Analysis**
1. Choose 3 companies in your target industry
2. Compare their business models, strategies, and market positions
3. Analyze their recent news and developments

**Week 3: Trend Deep Dive**
1. Select one emerging trend in your industry
2. Research its potential impact and timeline
3. Prepare a presentation on how professionals should adapt

**Final Project:**
Create an "Industry Intelligence Brief" (2-3 pages) that you would present to a new team member, covering key industry insights, trends, and strategic implications.''',
                'duration_weeks': 3,
                'difficulty_level': 'intermediate',
                'order_index': 2
            },
            {
                'title': 'Leadership and Team Management',
                'description': 'Develop essential leadership skills including team building, conflict resolution, and strategic thinking.',
                'content': '''# Leadership and Team Management

Leadership is not about titles or positions—it's about influence, vision, and the ability to inspire others toward common goals. This advanced module will develop your leadership capabilities.

## Core Leadership Principles

### 1. Self-Leadership
Before leading others, you must lead yourself:
- Self-awareness and emotional intelligence
- Personal values and leadership philosophy
- Continuous learning and growth mindset
- Resilience and stress management
- Decision-making frameworks

### 2. Vision and Strategy
Great leaders create compelling visions:
- Developing and communicating vision
- Strategic thinking and planning
- Aligning team goals with organizational objectives
- Change management and adaptation
- Innovation and creative problem-solving

### 3. Team Development
Building high-performing teams:
- Team formation and dynamics
- Delegation and empowerment
- Performance management and feedback
- Diversity, equity, and inclusion
- Conflict resolution and mediation

## Leadership Styles and Situations

### Situational Leadership
- Directing: High direction, low support
- Coaching: High direction, high support
- Supporting: Low direction, high support
- Delegating: Low direction, low support

### When to Use Each Style
Learn to adapt your leadership approach based on:
- Team member competence and commitment
- Task complexity and urgency
- Organizational culture and context
- Stakeholder expectations

## Communication and Influence

### Effective Communication
- Active listening and empathy
- Clear and compelling messaging
- Nonverbal communication awareness
- Difficult conversations and feedback
- Public speaking and presentation skills

### Building Influence
- Credibility and trust building
- Persuasion and negotiation
- Relationship management
- Network leverage
- Social capital development

## Team Performance Optimization

### Creating Psychological Safety
- Encouraging open communication
- Learning from failures
- Inclusive decision-making
- Recognition and appreciation
- Work-life balance support

### Performance Management
- Setting clear expectations
- Regular check-ins and feedback
- Performance improvement plans
- Career development discussions
- Succession planning''',
                'learning_objectives': '''- Develop self-awareness and emotional intelligence as foundation for leadership
- Create and communicate compelling vision and strategy
- Build and lead high-performing, diverse teams
- Master situational leadership and adapt style to context
- Handle conflicts and difficult situations with confidence
- Influence and motivate others without formal authority''',
                'resources': '''**Essential Leadership Books:**
- "The Leadership Challenge" by Kouzes & Posner
- "Emotional Intelligence" by Daniel Goleman
- "Start with Why" by Simon Sinek
- "The Five Dysfunctions of a Team" by Patrick Lencioni

**Assessment Tools:**
- StrengthsFinder 2.0
- DISC Leadership Assessment
- 360-degree feedback tools
- Emotional Intelligence assessments

**Online Learning:**
- Harvard Business School Online: Leadership courses
- LinkedIn Learning: Management and Leadership
- MasterClass: Leadership lessons from experts
- Coursera: Leadership specializations

**Practical Resources:**
- Team charter templates
- One-on-one meeting guides
- Performance review frameworks
- Conflict resolution strategies''',
                'assignments': '''**Week 1: Leadership Self-Assessment**
1. Complete leadership style assessment
2. Gather 360-degree feedback from colleagues
3. Develop personal leadership philosophy statement
4. Create leadership development plan

**Week 2: Team Analysis and Development**
1. Analyze a team you lead or participate in
2. Identify team dynamics and areas for improvement
3. Develop team charter or improvement plan
4. Practice difficult conversation scenarios

**Week 3: Vision and Strategy Development**
1. Create vision statement for your team/department
2. Develop strategic plan with measurable goals
3. Design communication strategy for vision rollout
4. Present vision to mentor for feedback

**Week 4: Leadership in Action**
1. Implement one leadership initiative
2. Document challenges and lessons learned
3. Seek feedback from team members
4. Adjust approach based on results

**Capstone Project:**
Lead a real project or initiative, applying leadership principles learned. Document your leadership journey, challenges faced, and growth achieved. Present findings to mentor group.''',
                'duration_weeks': 4,
                'difficulty_level': 'advanced',
                'order_index': 3
            },
            {
                'title': 'Digital Skills and Technology Adaptation',
                'description': 'Master essential digital tools and develop strategies for continuous technology learning.',
                'content': '''# Digital Skills and Technology Adaptation

In today's rapidly evolving digital landscape, technological fluency is essential for professional success across all industries. This module will help you develop both technical skills and the mindset for continuous learning.

## Digital Literacy Foundation

### Core Digital Skills
- Computer fundamentals and troubleshooting
- Internet research and information evaluation
- Cloud computing and file management
- Cybersecurity awareness and best practices
- Digital communication tools and etiquette

### Information Management
- Data organization and file naming conventions
- Version control for documents and projects
- Backup strategies and disaster recovery
- Privacy settings and data protection
- Digital asset management

## Professional Software Proficiency

### Productivity Suites
**Microsoft Office 365 / Google Workspace:**
- Advanced document creation and formatting
- Spreadsheet analysis and visualization
- Presentation design and delivery
- Collaborative editing and sharing
- Automation with templates and macros

### Specialized Tools by Function
**Project Management:**
- Asana, Trello, Monday.com
- Gantt charts and timeline management
- Resource allocation and tracking
- Agile and Scrum methodologies

**Communication and Collaboration:**
- Slack, Microsoft Teams, Zoom
- Video conferencing best practices
- Virtual meeting facilitation
- Cross-timezone collaboration

**Creative and Design:**
- Canva, Adobe Creative Suite basics
- Visual storytelling and infographics
- Brand consistency and templates
- Basic photo and video editing

## Emerging Technologies

### Artificial Intelligence and Automation
- Understanding AI capabilities and limitations
- Using AI tools for productivity (ChatGPT, Jasper, etc.)
- Automation opportunities in your role
- Ethical considerations in AI adoption

### Data Analytics and Visualization
- Excel/Google Sheets advanced functions
- Introduction to Tableau or Power BI
- Basic SQL for data queries
- Dashboard creation and maintenance
- Data-driven decision making

### Digital Marketing and Social Media
- Social media platform strategies
- Content creation and curation
- Basic analytics and metrics
- Online reputation management
- Digital advertising fundamentals

## Technology Learning Strategies

### Continuous Learning Framework
1. **Assess Current Skills**: Regular skills audit
2. **Identify Gaps**: Compare with industry requirements
3. **Prioritize Learning**: Focus on high-impact skills
4. **Practice Regularly**: Hands-on application
5. **Stay Updated**: Follow technology trends

### Learning Resources
- Online learning platforms (Coursera, Udemy, LinkedIn Learning)
- YouTube tutorials and channels
- Professional certification programs
- Vendor-specific training (Microsoft, Google, Adobe)
- Peer learning and study groups

### Staying Current
- Technology news sources (TechCrunch, Wired, MIT Technology Review)
- Industry-specific technology publications
- Webinars and virtual conferences
- Professional association resources
- Technology meetups and user groups''',
                'learning_objectives': '''- Demonstrate proficiency in essential digital tools and platforms
- Develop systematic approach to learning new technologies
- Apply digital skills to improve work efficiency and effectiveness
- Understand emerging technology trends and their workplace implications
- Create personal technology learning and adaptation strategy
- Evaluate and select appropriate tools for specific tasks and projects''',
                'resources': '''**Online Learning Platforms:**
- LinkedIn Learning: Technology courses library
- Coursera: Technology specializations from top universities
- Udemy: Practical technology skills courses
- Khan Academy: Computer programming and digital literacy
- Microsoft Learn: Free Microsoft technology training

**Certification Programs:**
- Microsoft Office Specialist (MOS)
- Google Workspace certification
- Adobe Certified Expert (ACE)
- CompTIA IT Fundamentals+
- HubSpot Content Marketing certification

**Technology News and Trends:**
- TechCrunch, The Verge, Ars Technica
- Harvard Business Review: Technology section
- MIT Technology Review
- Gartner research and reports
- Industry-specific technology publications

**Practice Platforms:**
- Sandbox environments for software testing
- Free trial versions of professional software
- Open-source alternatives for learning
- Kaggle for data science practice
- GitHub for version control learning''',
                'assignments': '''**Week 1: Digital Skills Assessment and Planning**
1. Complete comprehensive digital skills assessment
2. Identify 3 priority areas for improvement
3. Research learning resources for chosen skills
4. Create personal technology learning plan

**Week 2: Productivity Tools Mastery**
1. Choose one productivity suite to master
2. Complete advanced tutorials and practice exercises
3. Create templates for common work tasks
4. Automate one repetitive process

**Week 3: Emerging Technology Exploration**
1. Research one emerging technology relevant to your field
2. Test 3 new digital tools or platforms
3. Write comparative analysis of tools tested
4. Present findings to your mentor group

**Week 4: Technology Implementation Project**
1. Implement new digital solution for a work challenge
2. Document process and measure improvement
3. Train others on the solution if applicable
4. Create case study of technology adoption

**Final Portfolio:**
Create a "Digital Competency Portfolio" showcasing:
- Skills assessment results and growth
- Projects completed using digital tools
- Technology recommendations for your role/industry
- Personal continuous learning strategy''',
                'duration_weeks': 4,
                'difficulty_level': 'intermediate',
                'order_index': 4
            }
        ]
        
        created_modules = []
        
        for module_data in modules_data:
            # Check if module already exists
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
                print(f"Created curriculum module: {module.title}")
        
        db.session.commit()
        
        print(f"\nSample curriculum creation completed!")
        print(f"Created {len(created_modules)} curriculum modules:")
        for module in created_modules:
            print(f"- {module.title} ({module.difficulty_level}, {module.duration_weeks} weeks)")
        
        print("\nCurriculum modules are now available for:")
        print("- Admins to manage and edit")
        print("- Mentors to deliver to their groups")
        print("- Students to access and complete assignments")

if __name__ == '__main__':
    create_sample_curriculum()