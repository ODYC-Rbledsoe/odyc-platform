from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import CareerPathway, Industry

survey_bp = Blueprint('survey', __name__, url_prefix='/survey')

@survey_bp.route('/')
@login_required
def index():
    """Display the career interest survey form"""
    return render_template('survey.html')

@survey_bp.route('/submit', methods=['POST'])
@login_required
def submit():
    """Process survey results and show recommendations"""
    
    # Get survey responses
    learning_style = request.form.get('learning_style')
    work_environment = request.form.getlist('work_environment')
    interests = request.form.getlist('interests')
    favorite_subjects = request.form.getlist('favorite_subjects')
    motivation = request.form.get('motivation')
    physical_activity = request.form.get('physical_activity')
    problem_solving = request.form.get('problem_solving')
    teamwork = request.form.get('teamwork')
    
    # Calculate career pathway recommendations based on responses
    recommendations = calculate_recommendations({
        'learning_style': learning_style,
        'work_environment': work_environment,
        'interests': interests,
        'favorite_subjects': favorite_subjects,
        'motivation': motivation,
        'physical_activity': physical_activity,
        'problem_solving': problem_solving,
        'teamwork': teamwork
    })
    
    return render_template('survey_results.html', 
                         recommendations=recommendations,
                         user_responses={
                             'learning_style': learning_style,
                             'work_environment': work_environment,
                             'interests': interests,
                             'favorite_subjects': favorite_subjects,
                             'motivation': motivation,
                             'physical_activity': physical_activity,
                             'problem_solving': problem_solving,
                             'teamwork': teamwork
                         })

def calculate_recommendations(responses):
    """Calculate career pathway recommendations based on survey responses"""
    
    # Define scoring weights for each career pathway
    pathway_scores = {
        'electrical_instrumentation': 0,
        'process_operator': 0,
        'mechanical_maintenance': 0,
        'healthcare_medical': 0
    }
    
    # Learning style scoring
    if responses['learning_style'] == 'hands_on':
        pathway_scores['electrical_instrumentation'] += 3
        pathway_scores['mechanical_maintenance'] += 3
        pathway_scores['process_operator'] += 2
    elif responses['learning_style'] == 'visual':
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['healthcare_medical'] += 2
    elif responses['learning_style'] == 'analytical':
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['process_operator'] += 3
    elif responses['learning_style'] == 'collaborative':
        pathway_scores['healthcare_medical'] += 3
        pathway_scores['process_operator'] += 2
    
    # Work environment scoring
    work_env = responses['work_environment']
    if 'industrial' in work_env:
        pathway_scores['electrical_instrumentation'] += 3
        pathway_scores['mechanical_maintenance'] += 3
        pathway_scores['process_operator'] += 3
    if 'office' in work_env:
        pathway_scores['healthcare_medical'] += 2
    if 'outdoor' in work_env:
        pathway_scores['mechanical_maintenance'] += 2
        pathway_scores['process_operator'] += 2
    if 'laboratory' in work_env:
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['healthcare_medical'] += 3
    if 'healthcare' in work_env:
        pathway_scores['healthcare_medical'] += 4
    
    # Interests scoring
    interests = responses['interests']
    if 'technology' in interests:
        pathway_scores['electrical_instrumentation'] += 3
    if 'engineering' in interests:
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['mechanical_maintenance'] += 2
    if 'manufacturing' in interests:
        pathway_scores['process_operator'] += 3
        pathway_scores['mechanical_maintenance'] += 2
    if 'healthcare' in interests:
        pathway_scores['healthcare_medical'] += 4
    if 'problem_solving' in interests:
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['mechanical_maintenance'] += 2
    if 'helping_people' in interests:
        pathway_scores['healthcare_medical'] += 3
    
    # Favorite subjects scoring
    subjects = responses['favorite_subjects']
    if 'math' in subjects:
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['process_operator'] += 2
    if 'science' in subjects:
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['process_operator'] += 2
        pathway_scores['healthcare_medical'] += 2
    if 'biology' in subjects:
        pathway_scores['healthcare_medical'] += 3
    if 'physics' in subjects:
        pathway_scores['electrical_instrumentation'] += 3
        pathway_scores['mechanical_maintenance'] += 2
    if 'chemistry' in subjects:
        pathway_scores['process_operator'] += 3
        pathway_scores['healthcare_medical'] += 2
    if 'computer_science' in subjects:
        pathway_scores['electrical_instrumentation'] += 3
    
    # Physical activity preference
    if responses['physical_activity'] == 'very_active':
        pathway_scores['mechanical_maintenance'] += 3
        pathway_scores['process_operator'] += 2
    elif responses['physical_activity'] == 'moderately_active':
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['healthcare_medical'] += 2
    
    # Problem solving preference
    if responses['problem_solving'] == 'technical':
        pathway_scores['electrical_instrumentation'] += 3
        pathway_scores['mechanical_maintenance'] += 2
    elif responses['problem_solving'] == 'process':
        pathway_scores['process_operator'] += 3
    elif responses['problem_solving'] == 'people':
        pathway_scores['healthcare_medical'] += 3
    
    # Teamwork preference
    if responses['teamwork'] == 'team_leader':
        pathway_scores['process_operator'] += 2
        pathway_scores['healthcare_medical'] += 2
    elif responses['teamwork'] == 'team_member':
        pathway_scores['electrical_instrumentation'] += 2
        pathway_scores['mechanical_maintenance'] += 2
    
    # Sort pathways by score and get top 3
    sorted_pathways = sorted(pathway_scores.items(), key=lambda x: x[1], reverse=True)
    top_pathways = sorted_pathways[:3]
    
    # Create recommendation objects
    recommendations = []
    
    pathway_data = {
        'electrical_instrumentation': {
            'title': 'Electrical & Instrumentation Technician',
            'description': 'Design, install, and maintain electrical systems and industrial automation equipment',
            'salary_range': '$45,000 - $75,000',
            'icon': 'fas fa-bolt',
            'skills': ['Circuit Analysis', 'PLC Programming', 'SCADA Systems', 'Electrical Safety'],
            'employers': ['Genesis Alkali', 'Bridger Coal Company', 'Rocky Mountain Power'],
            'education': 'Associate Degree in Electrical Technology or related field'
        },
        'process_operator': {
            'title': 'Process Operator',
            'description': 'Monitor and control industrial processes in manufacturing and chemical plants',
            'salary_range': '$50,000 - $80,000',
            'icon': 'fas fa-industry',
            'skills': ['Process Control', 'Safety Protocols', 'Equipment Operation', 'Quality Control'],
            'employers': ['Genesis Alkali', 'Bridger Coal Company', 'Local Manufacturing'],
            'education': 'High School Diploma + On-the-job Training or Certificate Program'
        },
        'mechanical_maintenance': {
            'title': 'Mechanical Maintenance Technician',
            'description': 'Maintain, repair, and troubleshoot mechanical equipment and machinery',
            'salary_range': '$40,000 - $70,000',
            'icon': 'fas fa-wrench',
            'skills': ['Hydraulics', 'Pneumatics', 'Welding', 'Preventive Maintenance'],
            'employers': ['Wyoming Machine Works', 'Bridger Coal Company', 'Local Industries'],
            'education': 'Certificate Program or Associate Degree in Mechanical Technology'
        },
        'healthcare_medical': {
            'title': 'Healthcare & Medical Technician',
            'description': 'Provide healthcare services and support in medical facilities',
            'salary_range': '$35,000 - $65,000',
            'icon': 'fas fa-heartbeat',
            'skills': ['Patient Care', 'Medical Equipment', 'Health Records', 'Communication'],
            'employers': ['Memorial Hospital', 'Local Clinics', 'Healthcare Facilities'],
            'education': 'Certificate Program or Associate Degree in Healthcare'
        }
    }
    
    for pathway_id, score in top_pathways:
        if score > 0:  # Only include pathways with positive scores
            pathway_info = pathway_data.get(pathway_id)
            if pathway_info:
                pathway_info['match_score'] = min(100, int((score / 15) * 100))  # Convert to percentage
                recommendations.append(pathway_info)
    
    # Ensure we have at least 2 recommendations
    if len(recommendations) < 2:
        # Add fallback recommendations
        for pathway_id, pathway_info in pathway_data.items():
            if pathway_id not in [rec.get('title', '').lower().replace(' ', '_').replace('&', '').replace('technician', '').strip('_') for rec in recommendations]:
                pathway_info['match_score'] = 50  # Default match score
                recommendations.append(pathway_info)
                if len(recommendations) >= 3:
                    break
    
    return recommendations[:3]