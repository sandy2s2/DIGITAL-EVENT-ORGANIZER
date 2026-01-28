"""
Event Routes
Handles event-related public routes
"""

from flask import Blueprint, render_template, request, jsonify
from app.controllers.event_controller import EventController

# Create Blueprint
event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/')
def list_events():
    """Public events listing page"""
    events = EventController.get_upcoming_events()
    return render_template('user/events.html', events=events)

@event_bp.route('/<int:event_id>')
def view_event(event_id):
    """Public event details page"""
    event = EventController.get_event_details(event_id)
    
    if not event:
        return "Event not found", 404
    
    return render_template('user/event_details.html', event=event)

@event_bp.route('/category/<category>')
def events_by_category(category):
    """Events filtered by category"""
    events = EventController.get_events_by_category(category)
    return render_template('user/events.html', events=events, category=category)

@event_bp.route('/search')
def search_events():
    """Search events"""
    keyword = request.args.get('q', '')
    events = EventController.search_events(keyword)
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'events': events
        })
    
    return render_template('user/events.html', events=events, search=keyword)
