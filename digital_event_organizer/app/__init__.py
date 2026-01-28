"""
Flask Application Factory
Creates and configures the Flask application instance
"""

from flask import Flask
from flask_mail import Mail
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask-Mail
mail = Mail()

def create_app():
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'digital_event_organizer')
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', '')
    
    # Payment configuration
    app.config['RAZORPAY_KEY_ID'] = os.getenv('RAZORPAY_KEY_ID', '')
    app.config['RAZORPAY_KEY_SECRET'] = os.getenv('RAZORPAY_KEY_SECRET', '')
    
    # Initialize extensions
    mail.init_app(app)
    
    # Register blueprints (routes)
    from app.routes import user_routes, admin_routes, event_routes, payment_routes
    
    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(admin_routes.admin_bp)
    app.register_blueprint(event_routes.event_bp)
    app.register_blueprint(payment_routes.payment_bp)
    
    # Home route
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('user/login.html')
    
    return app
