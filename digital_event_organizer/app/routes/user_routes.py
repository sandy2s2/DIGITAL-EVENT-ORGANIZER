"""
User Routes
Handles all user-related HTTP routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers.user_controller import UserController
from app.controllers.event_controller import EventController
from functools import wraps

# Create Blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        # Register user
        success, message, user_id = UserController.register_user(name, email, password, phone)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('user.login'))
        else:
            flash(message, 'danger')
    
    return render_template('user/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authenticate user
        success, message, user = UserController.login_user(email, password)
        
        if success:
            # Store user info in session
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            
            flash(message, 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash(message, 'danger')
    
    return render_template('user/login.html')

@user_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_id = session.get('user_id')
    
    # Get user's registrations
    registrations = UserController.get_user_registrations(user_id)
    
    # Get upcoming events
    upcoming_events = EventController.get_upcoming_events()
    
    return render_template('user/dashboard.html', 
                         registrations=registrations,
                         upcoming_events=upcoming_events[:5])  # Show 5 latest

@user_bp.route('/events')
@login_required
def events():
    """View all events"""
    # Get search and filter parameters
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    if search:
        events_list = EventController.search_events(search)
    elif category:
        events_list = EventController.get_events_by_category(category)
    else:
        events_list = EventController.get_upcoming_events()
    
    return render_template('user/events.html', events=events_list, 
                         search=search, category=category)

@user_bp.route('/events/<int:event_id>')
@login_required
def event_details(event_id):
    """View event details"""
    event = EventController.get_event_details(event_id)
    
    if not event:
        flash('Event not found', 'danger')
        return redirect(url_for('user.events'))
    
    user_id = session.get('user_id')
    from app.models.registration import Registration
    is_registered = Registration.is_user_registered(user_id, event_id)
    
    return render_template('user/event_details.html', 
                         event=event, 
                         is_registered=is_registered)

@user_bp.route('/events/<int:event_id>/register', methods=['POST'])
@login_required
def register_event(event_id):
    """Register for an event"""
    user_id = session.get('user_id')
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    
    success, message, data = EventController.register_for_event(
        user_id, event_id, user_email, user_name
    )
    
    if success:
        # Check if payment is required
        if isinstance(data, dict) and data.get('payment_required'):
            # Redirect to payment page
            session['payment_data'] = data
            flash('Please complete payment to confirm registration', 'info')
            return redirect(url_for('payment.initiate', registration_id=data['registration_id']))
        else:
            flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('user.event_details', event_id=event_id))

@user_bp.route('/registrations')
@login_required
def my_registrations():
    """View user's registrations"""
    user_id = session.get('user_id')
    registrations = UserController.get_user_registrations(user_id)
    
    return render_template('user/my_registrations.html', registrations=registrations)

@user_bp.route('/profile')
@login_required
def profile():
    """View user profile"""
    user_id = session.get('user_id')
    user = UserController.get_user_profile(user_id)
    
    return render_template('user/profile.html', user=user)

@user_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    user_id = session.get('user_id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    
    success, message = UserController.update_user_profile(user_id, name, phone)
    
    if success:
        session['user_name'] = name
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('user.profile'))
