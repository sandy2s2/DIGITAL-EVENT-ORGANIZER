"""
Event Model
Handles all event-related database operations
"""

from app.utils.db_config import execute_query, execute_one

class Event:
    """Event model for database operations"""
    
    @staticmethod
    def create_event(title, description, event_date, event_time, venue, category, 
                     price=0.0, is_paid=False, max_participants=100, 
                     registration_deadline=None, created_by=None):
        """
        Create a new event
        
        Args:
            title: Event title
            description: Event description
            event_date: Event date (YYYY-MM-DD)
            event_time: Event time (HH:MM:SS)
            venue: Event venue
            category: Event category
            price: Event price (default 0.0)
            is_paid: Is paid event (default False)
            max_participants: Maximum participants (default 100)
            registration_deadline: Registration deadline date
            created_by: Admin user ID who created the event
        
        Returns:
            event_id if successful, None otherwise
        """
        query = """
            INSERT INTO events 
            (title, description, event_date, event_time, venue, category, 
             price, is_paid, max_participants, registration_deadline, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, description, event_date, event_time, venue, category,
                 price, is_paid, max_participants, registration_deadline, created_by)
        
        return execute_query(query, params)
    
    @staticmethod
    def get_all_events():
        """
        Get all events
        
        Returns:
            List of event dictionaries
        """
        query = """
            SELECT * FROM events 
            ORDER BY event_date ASC, event_time ASC
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_upcoming_events():
        """
        Get upcoming events (future events only)
        
        Returns:
            List of upcoming event dictionaries
        """
        query = """
            SELECT * FROM events 
            WHERE event_date >= CURDATE()
            ORDER BY event_date ASC, event_time ASC
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_event_by_id(event_id):
        """
        Get event by ID
        
        Args:
            event_id: Event ID
        
        Returns:
            Event dictionary or None
        """
        query = "SELECT * FROM events WHERE event_id = %s"
        return execute_one(query, (event_id,))
    
    @staticmethod
    def get_events_by_category(category):
        """
        Get events by category
        
        Args:
            category: Event category
        
        Returns:
            List of event dictionaries
        """
        query = """
            SELECT * FROM events 
            WHERE category = %s AND event_date >= CURDATE()
            ORDER BY event_date ASC
        """
        return execute_query(query, (category,), fetch=True)
    
    @staticmethod
    def update_event(event_id, **kwargs):
        """
        Update event details
        
        Args:
            event_id: Event ID
            **kwargs: Fields to update (title, description, etc.)
        
        Returns:
            Number of affected rows
        """
        allowed_fields = ['title', 'description', 'event_date', 'event_time', 
                         'venue', 'category', 'price', 'is_paid', 
                         'max_participants', 'registration_deadline']
        
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                updates.append(f"{field} = %s")
                params.append(value)
        
        if not updates:
            return 0
        
        params.append(event_id)
        query = f"UPDATE events SET {', '.join(updates)} WHERE event_id = %s"
        
        return execute_query(query, tuple(params))
    
    @staticmethod
    def delete_event(event_id):
        """
        Delete an event
        
        Args:
            event_id: Event ID
        
        Returns:
            Number of affected rows
        """
        query = "DELETE FROM events WHERE event_id = %s"
        return execute_query(query, (event_id,))
    
    @staticmethod
    def increment_participants(event_id):
        """
        Increment current participants count
        
        Args:
            event_id: Event ID
        
        Returns:
            Number of affected rows
        """
        query = "UPDATE events SET current_participants = current_participants + 1 WHERE event_id = %s"
        return execute_query(query, (event_id,))
    
    @staticmethod
    def decrement_participants(event_id):
        """
        Decrement current participants count
        
        Args:
            event_id: Event ID
        
        Returns:
            Number of affected rows
        """
        query = "UPDATE events SET current_participants = current_participants - 1 WHERE event_id = %s AND current_participants > 0"
        return execute_query(query, (event_id,))
    
    @staticmethod
    def is_event_full(event_id):
        """
        Check if event has reached maximum participants
        
        Args:
            event_id: Event ID
        
        Returns:
            Boolean: True if event is full
        """
        event = Event.get_event_by_id(event_id)
        if not event:
            return True
        
        return event['current_participants'] >= event['max_participants']
    
    @staticmethod
    def get_available_seats(event_id):
        """
        Get number of available seats
        
        Args:
            event_id: Event ID
        
        Returns:
            Number of available seats
        """
        event = Event.get_event_by_id(event_id)
        if not event:
            return 0
        
        return event['max_participants'] - event['current_participants']
