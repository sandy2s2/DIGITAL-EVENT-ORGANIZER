"""
Event Controller
Handles event-related business logic
"""

from app.models.event import Event
from app.models.registration import Registration
from app.utils.validators import validate_date, validate_time, validate_required_fields
from app.utils.email_service import send_registration_confirmation
from datetime import datetime

class EventController:
    """Controller for event operations"""
    
    @staticmethod
    def create_event(data, admin_id):
        """
        Create a new event
        
        Args:
            data: Dictionary with event details
            admin_id: Admin user ID
        
        Returns:
            Tuple: (success: Boolean, message: str, event_id: int or None)
        """
        # Required fields
        required = ['title', 'description', 'event_date', 'event_time', 
                   'venue', 'category']
        
        valid, missing = validate_required_fields(data, required)
        if not valid:
            return False, f"Missing required fields: {', '.join(missing)}", None
        
        # Validate date and time
        if not validate_date(data['event_date']):
            return False, "Invalid date format (use YYYY-MM-DD)", None
        
        if not validate_time(data['event_time']):
            return False, "Invalid time format (use HH:MM)", None
        
        # Parse optional fields
        price = float(data.get('price', 0.0))
        is_paid = data.get('is_paid', 'false').lower() == 'true'
        max_participants = int(data.get('max_participants', 100))
        registration_deadline = data.get('registration_deadline', None)
        
        # Validate registration deadline if provided
        if registration_deadline and not validate_date(registration_deadline):
            return False, "Invalid registration deadline format", None
        
        # Create event
        event_id = Event.create_event(
            title=data['title'].strip(),
            description=data['description'].strip(),
            event_date=data['event_date'],
            event_time=data['event_time'],
            venue=data['venue'].strip(),
            category=data['category'].strip(),
            price=price,
            is_paid=is_paid,
            max_participants=max_participants,
            registration_deadline=registration_deadline,
            created_by=admin_id
        )
        
        if event_id:
            return True, "Event created successfully", event_id
        else:
            return False, "Failed to create event", None
    
    @staticmethod
    def update_event(event_id, data):
        """
        Update an existing event
        
        Args:
            event_id: Event ID
            data: Dictionary with updated fields
        
        Returns:
            Tuple: (success: Boolean, message: str)
        """
        # Validate date if provided
        if 'event_date' in data and not validate_date(data['event_date']):
            return False, "Invalid date format"
        
        # Validate time if provided
        if 'event_time' in data and not validate_time(data['event_time']):
            return False, "Invalid time format"
        
        # Update event
        affected = Event.update_event(event_id, **data)
        
        if affected:
            return True, "Event updated successfully"
        else:
            return False, "No changes made or event not found"
    
    @staticmethod
    def delete_event(event_id):
        """
        Delete an event
        
        Args:
            event_id: Event ID
        
        Returns:
            Tuple: (success: Boolean, message: str)
        """
        affected = Event.delete_event(event_id)
        
        if affected:
            return True, "Event deleted successfully"
        else:
            return False, "Event not found or already deleted"
    
    @staticmethod
    def get_all_events():
        """
        Get all events
        
        Returns:
            List of events
        """
        return Event.get_all_events()
    
    @staticmethod
    def get_upcoming_events():
        """
        Get upcoming events only
        
        Returns:
            List of upcoming events
        """
        return Event.get_upcoming_events()
    
    @staticmethod
    def get_event_details(event_id):
        """
        Get event details by ID
        
        Args:
            event_id: Event ID
        
        Returns:
            Event dictionary or None
        """
        return Event.get_event_by_id(event_id)
    
    @staticmethod
    def register_for_event(user_id, event_id, user_email, user_name):
        """
        Register a user for an event
        
        Args:
            user_id: User ID
            event_id: Event ID
            user_email: User's email for confirmation
            user_name: User's name
        
        Returns:
            Tuple: (success: Boolean, message: str, registration_id or payment_required)
        """
        # Get event details
        event = Event.get_event_by_id(event_id)
        
        if not event:
            return False, "Event not found", None
        
        # Check if event is full
        if Event.is_event_full(event_id):
            return False, "Event is full. No more seats available.", None
        
        # Check if user already registered
        if Registration.is_user_registered(user_id, event_id):
            return False, "You are already registered for this event", None
        
        # Check registration deadline
        if event['registration_deadline']:
            deadline = datetime.strptime(str(event['registration_deadline']), '%Y-%m-%d')
            if datetime.now() > deadline:
                return False, "Registration deadline has passed", None
        
        # Check if payment is required
        payment_required = event['is_paid']
        
        # Create registration
        registration_id = Registration.create_registration(
            user_id=user_id,
            event_id=event_id,
            payment_required=payment_required
        )
        
        if not registration_id:
            return False, "Registration failed. Please try again.", None
        
        # Increment participant count
        Event.increment_participants(event_id)
        
        # If free event, send confirmation email
        if not payment_required:
            send_registration_confirmation(
                user_email=user_email,
                user_name=user_name,
                event_title=event['title'],
                event_date=str(event['event_date']),
                event_time=str(event['event_time']),
                venue=event['venue']
            )
            return True, "Registration successful!", registration_id
        else:
            # For paid events, return registration_id and indicate payment is needed
            return True, "Please complete payment to confirm registration", {
                'registration_id': registration_id,
                'payment_required': True,
                'amount': float(event['price'])
            }
    
    @staticmethod
    def cancel_registration(user_id, event_id):
        """
        Cancel a registration
        
        Args:
            user_id: User ID
            event_id: Event ID
        
        Returns:
            Tuple: (success: Boolean, message: str)
        """
        # Get registration
        registration = Registration.get_registration_by_user_event(user_id, event_id)
        
        if not registration:
            return False, "Registration not found"
        
        # Cancel registration
        affected = Registration.cancel_registration(registration['registration_id'])
        
        if affected:
            # Decrement participant count
            Event.decrement_participants(event_id)
            return True, "Registration cancelled successfully"
        else:
            return False, "Failed to cancel registration"
    
    @staticmethod
    def search_events(keyword):
        """
        Search events by keyword in title or description
        
        Args:
            keyword: Search keyword
        
        Returns:
            List of matching events
        """
        all_events = Event.get_upcoming_events()
        
        if not keyword:
            return all_events
        
        keyword = keyword.lower()
        filtered = []
        
        for event in all_events:
            if (keyword in event['title'].lower() or 
                keyword in event['description'].lower() or
                keyword in event['category'].lower()):
                filtered.append(event)
        
        return filtered
    
    @staticmethod
    def get_events_by_category(category):
        """
        Get events by category
        
        Args:
            category: Event category
        
        Returns:
            List of events in that category
        """
        return Event.get_events_by_category(category)
