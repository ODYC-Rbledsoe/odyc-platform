#!/usr/bin/env python3
"""
Seed script for National Career Clusters Framework (14 clusters)
Based on the modernized framework from careertech.org
"""

from app import app, db
from models import CareerCluster, Industry, JobRole, CareerPathway, EmployerPartner
import json

def seed_career_clusters():
    """Seed the 14 National Career Clusters with authentic data"""
    
    clusters_data = [
        {
            'name': 'Advanced Manufacturing',
            'description': 'Planning, managing and performing the processing of materials into intermediate or final products and related professional and technical support activities such as production planning and control, maintenance and manufacturing/process engineering.',
            'color_code': '#FF6B35',
            'icon_class': 'fas fa-industry',
            'is_priority_local': True  # High priority for Southwest Wyoming
        },
        {
            'name': 'Agriculture',
            'description': 'The production, processing, marketing, distribution, financing, and development of agricultural commodities and resources including food, fiber, wood products, natural resources, horticulture, and other plant and animal products/resources.',
            'color_code': '#4CAF50',
            'icon_class': 'fas fa-tractor',
            'is_priority_local': False
        },
        {
            'name': 'Arts, Entertainment, & Design',
            'description': 'Designing, producing, exhibiting, performing, writing, and publishing multimedia content including visual and performing arts and design, journalism, and entertainment services.',
            'color_code': '#9C27B0',
            'icon_class': 'fas fa-palette',
            'is_priority_local': False
        },
        {
            'name': 'Construction',
            'description': 'Careers in designing, planning, managing, building and maintaining the built environment.',
            'color_code': '#FF9800',
            'icon_class': 'fas fa-hard-hat',
            'is_priority_local': True  # Growing sector in Wyoming
        },
        {
            'name': 'Digital Technology',
            'description': 'Building linkages in IT occupations framework for entry level, technical and professional careers related to the design, development, support and management of hardware, software, multimedia and systems integration services.',
            'color_code': '#2196F3',
            'icon_class': 'fas fa-laptop-code',
            'is_priority_local': False
        },
        {
            'name': 'Education',
            'description': 'Planning, managing and providing education and training services, and related learning support services.',
            'color_code': '#795548',
            'icon_class': 'fas fa-graduation-cap',
            'is_priority_local': True  # Education is priority for ODYC mission
        },
        {
            'name': 'Energy & Natural Resources',
            'description': 'Careers in the production, transmission and distribution of electricity, natural gas, oil and other energy sources, as well as careers related to extraction, production and distribution of natural resources.',
            'color_code': '#607D8B',
            'icon_class': 'fas fa-bolt',
            'is_priority_local': True  # Critical for Wyoming's economy
        },
        {
            'name': 'Financial Services',
            'description': 'Planning, services for financial and investment planning, banking, insurance, and business financial management.',
            'color_code': '#4CAF50',
            'icon_class': 'fas fa-dollar-sign',
            'is_priority_local': False
        },
        {
            'name': 'Healthcare & Human Services',
            'description': 'Planning, managing, and providing therapeutic services, diagnostic services, health informatics, support services, and biotechnology research and development.',
            'color_code': '#F44336',
            'icon_class': 'fas fa-heartbeat',
            'is_priority_local': True  # Sweetwater Memorial partnership
        },
        {
            'name': 'Hospitality, Events, & Tourism',
            'description': 'Hospitality & Tourism encompasses the management, marketing and operations of restaurants and other food services, lodging, attractions, recreation events and travel related services.',
            'color_code': '#E91E63',
            'icon_class': 'fas fa-concierge-bell',
            'is_priority_local': False
        },
        {
            'name': 'Management & Entrepreneurship',
            'description': 'Planning, organizing, directing and evaluating business functions essential to efficient and productive business operations. Entrepreneurship is included as owning and operating one\'s own business or starting a new venture for an existing business.',
            'color_code': '#673AB7',
            'icon_class': 'fas fa-chart-line',
            'is_priority_local': False
        },
        {
            'name': 'Marketing & Sales',
            'description': 'Planning, managing, and performing marketing activities to reach organizational objectives.',
            'color_code': '#FF5722',
            'icon_class': 'fas fa-bullhorn',
            'is_priority_local': False
        },
        {
            'name': 'Public Service & Safety',
            'description': 'Executing governmental functions to include Governance; National Security; Foreign Service; Planning; Revenue and Taxation; Regulation; and Management and Administration at the local, state, and federal levels.',
            'color_code': '#3F51B5',
            'icon_class': 'fas fa-shield-alt',
            'is_priority_local': False
        },
        {
            'name': 'Supply Chain & Transportation',
            'description': 'Planning, management, and movement of people, materials, and goods by road, pipeline, air, rail and water and related professional and technical support services such as transportation infrastructure planning and management, logistics services, mobile equipment and facility maintenance.',
            'color_code': '#009688',
            'icon_class': 'fas fa-truck',
            'is_priority_local': True  # Important for rural Wyoming
        }
    ]
    
    print("Seeding Career Clusters...")
    
    for cluster_data in clusters_data:
        # Check if cluster already exists
        existing_cluster = CareerCluster.query.filter_by(name=cluster_data['name']).first()
        if not existing_cluster:
            cluster = CareerCluster(**cluster_data)
            db.session.add(cluster)
            print(f"Added cluster: {cluster_data['name']}")
        else:
            print(f"Cluster already exists: {cluster_data['name']}")
    
    try:
        db.session.commit()
        print("Career Clusters seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding career clusters: {e}")

def update_industries_with_clusters():
    """Update existing industries to link to career clusters"""
    
    # Mapping of existing industries to career clusters
    industry_cluster_mapping = {
        'Manufacturing': 'Advanced Manufacturing',
        'Energy & Mining': 'Energy & Natural Resources',
        'Healthcare': 'Healthcare & Human Services', 
        'Transportation & Logistics': 'Supply Chain & Transportation',
        'Construction & Trades': 'Construction'
    }
    
    print("Updating industries with career cluster links...")
    
    for industry_name, cluster_name in industry_cluster_mapping.items():
        industry = Industry.query.filter_by(name=industry_name).first()
        cluster = CareerCluster.query.filter_by(name=cluster_name).first()
        
        if industry and cluster:
            industry.career_cluster_id = cluster.id
            print(f"Linked {industry_name} to {cluster_name}")
        elif not industry:
            print(f"Industry not found: {industry_name}")
        elif not cluster:
            print(f"Cluster not found: {cluster_name}")
    
    try:
        db.session.commit()
        print("Industry-cluster links updated successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating industry links: {e}")

def main():
    """Run the seeding process"""
    with app.app_context():
        seed_career_clusters()
        update_industries_with_clusters()
        
        # Display summary
        cluster_count = CareerCluster.query.count()
        priority_clusters = CareerCluster.query.filter_by(is_priority_local=True).count()
        
        print(f"\n=== Career Clusters Summary ===")
        print(f"Total clusters: {cluster_count}")
        print(f"Priority clusters for Southwest Wyoming: {priority_clusters}")
        
        print(f"\nPriority clusters:")
        for cluster in CareerCluster.query.filter_by(is_priority_local=True).all():
            print(f"  - {cluster.name}")

if __name__ == "__main__":
    main()