import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///mentorship.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["WTF_CSRF_ENABLED"] = True

# Initialize extensions
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Register blueprints
from auth import auth_bp
from dashboard import dashboard_bp
from admin import admin_bp
from curriculum import curriculum_bp
from career_pathways import career_bp
from employer import employer_bp
from routes.survey import survey_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(curriculum_bp)
app.register_blueprint(career_bp)
app.register_blueprint(employer_bp)
app.register_blueprint(survey_bp)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Create default admin user if it doesn't exist
    from models import User
    from werkzeug.security import generate_password_hash
    
    admin_user = User.query.filter_by(email='admin@mentorship.com').first()
    if not admin_user:
        admin_user = User(
            name='Admin User',
            email='admin@mentorship.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            bio='System Administrator',
            interests_expertise='Platform Management'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: admin@mentorship.com / admin123")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
