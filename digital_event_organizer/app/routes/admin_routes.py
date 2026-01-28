"""
Admin Routes
Handles all admin-related HTTP routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.admin_controller import AdminController
from app.controllers.event_controller import EventController
from functools import wraps

# Create Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator to require admin login
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authenticate admin
        success, message, admin = AdminController.admin_login(email, password)
        
        if success:
            # Store admin info in session
            session['user_id'] = admin['user_id']
            session['user_name'] = admin['name']
            session['user_email'] = admin['email']
            session['user_role'] = admin['role']
            
            flash(message, 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash(message, 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    stats = AdminController.get_dashboard_stats()
    recent_events = EventController.get_upcoming_events()[:5]
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_events=recent_events)

@admin_bp.route('/events')
@admin_required
def manage_events():
    """Manage all events"""
    events = AdminController.get_all_events()
    return render_template('admin/manage_events.html', events=events)

@admin_bp.route('/events/create', methods=['GET', 'POST'])
@admin_required
def create_event():
    """Create new event"""
    if request.method == 'POST':
        admin_id = session.get('user_id')
        
        # Get form data
        data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'event_date': request.form.get('event_date'),
            'event_time': request.form.get('event_time'),
            'venue': request.form.get('venue'),
            'category': request.form.get('category'),
            'price': request.form.get('price', 0),
            'is_paid': request.form.get('is_paid', 'false'),
            'max_participants': request.form.get('max_participants', 100),
            'registration_deadline': request.form.get('registration_deadline')
        }
        
        # Create event
        success, message, event_id = EventController.create_event(data, admin_id)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.manage_events'))
        else:
            flash(message, 'danger')
    
    return render_template('admin/create_event.html')

@admin_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    """Edit event"""
    event = EventController.get_event_details(event_id)
    
    if not event:
        flash('Event not found', 'danger')
        return redirect(url_for('admin.manage_events'))
    
    if request.method == 'POST':
        # Get form data
        data = {}
        
        if request.form.get('title'):
            data['title'] = request.form.get('title')
        if request.form.get('description'):
            data['description'] = request.form.get('description')
        if request.form.get('event_date'):
            data['event_date'] = request.form.get('event_date')
        if request.form.get('event_time'):
            data['event_time'] = request.form.get('event_time')
        if request.form.get('venue'):
            data['venue'] = request.form.get('venue')
        if request.form.get('category'):
            data['category'] = request.form.get('category')
        if request.form.get('price'):
            data['price'] = request.form.get('price')
        if request.form.get('max_participants'):
            data['max_participants'] = request.form.get('max_participants')
        if request.form.get('registration_deadline'):
            data['registration_deadline'] = request.form.get('registration_deadline')
        
        # Update event
        success, message = EventController.update_event(event_id, data)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.manage_events'))
        else:
            flash(message, 'danger')
    
    return render_template('admin/edit_event.html', event=event)

@admin_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@admin_required
def delete_event(event_id):
    """Delete event"""
    success, message = EventController.delete_event(event_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('admin.manage_events'))

@admin_bp.route('/events/<int:event_id>/participants')
@admin_required
def view_participants(event_id):
    """View event participants"""
    event = EventController.get_event_details(event_id)
    
    if not event:
        flash('Event not found', 'danger')
        return redirect(url_for('admin.manage_events'))
    
    participants = AdminController.get_event_participants(event_id)
    payments = AdminController.get_event_payments(event_id)
    
    return render_template('admin/view_participants.html', 
                         event=event, 
                         participants=participants,
                         payments=payments)

@admin_bp.route('/users')
@admin_required
def manage_users():
    """View all users"""
    users = AdminController.get_all_users()
    return render_template('admin/manage_users.html', users=users)
