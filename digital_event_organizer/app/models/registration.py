"""
Registration Model
Handles all registration-related database operations
"""

from app.utils.db_config import execute_query, execute_one

class Registration:
    """Registration model for database operations"""
    
    @staticmethod
    def create_registration(user_id, event_id, payment_required=False):
        """
        Create a new registration
        
        Args:
            user_id: User ID
            event_id: Event ID
            payment_required: Whether payment is required
        
        Returns:
            registration_id if successful, None otherwise
        """
        # Check if user already registered for this event
        if Registration.is_user_registered(user_id, event_id):
            return None
        
        query = """
            INSERT INTO registrations (user_id, event_id, status, payment_required)
            VALUES (%s, %s, %s, %s)
        """
        status = 'pending' if payment_required else 'confirmed'
        params = (user_id, event_id, status, payment_required)
        
        return execute_query(query, params)
    
    @staticmethod
    def get_registration_by_id(registration_id):
        """
        Get registration by ID
        
        Args:
            registration_id: Registration ID
        
        Returns:
            Registration dictionary or None
        """
        query = "SELECT * FROM registrations WHERE registration_id = %s"
        return execute_one(query, (registration_id,))
    
    @staticmethod
    def get_user_registrations(user_id):
        """
        Get all registrations for a user with event details
        
        Args:
            user_id: User ID
        
        Returns:
            List of registration dictionaries with event details
        """
        query = """
            SELECT r.*, e.title, e.description, e.event_date, e.event_time, 
                   e.venue, e.category, e.price
            FROM registrations r
            JOIN events e ON r.event_id = e.event_id
            WHERE r.user_id = %s
            ORDER BY r.registration_date DESC
        """
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_event_registrations(event_id):
        """
        Get all registrations for an event with user details
        
        Args:
            event_id: Event ID
        
        Returns:
            List of registration dictionaries with user details
        """
        query = """
            SELECT r.*, u.name, u.email, u.phone
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.event_id = %s
            ORDER BY r.registration_date DESC
        """
        return execute_query(query, (event_id,), fetch=True)
    
    @staticmethod
    def is_user_registered(user_id, event_id):
        """
        Check if user is already registered for an event
        
        Args:
            user_id: User ID
            event_id: Event ID
        
        Returns:
            Boolean: True if user is registered
        """
        query = """
            SELECT COUNT(*) as count 
            FROM registrations 
            WHERE user_id = %s AND event_id = %s
        """
        result = execute_one(query, (user_id, event_id))
        return result and result['count'] > 0
    
    @staticmethod
    def update_registration_status(registration_id, status):
        """
        Update registration status
        
        Args:
            registration_id: Registration ID
            status: New status ('pending', 'confirmed', 'cancelled')
        
        Returns:
            Number of affected rows
        """
        query = "UPDATE registrations SET status = %s WHERE registration_id = %s"
        return execute_query(query, (status, registration_id))
    
    @staticmethod
    def cancel_registration(registration_id):
        """
        Cancel a registration
        
        Args:
            registration_id: Registration ID
        
        Returns:
            Number of affected rows
        """
        return Registration.update_registration_status(registration_id, 'cancelled')
    
    @staticmethod
    def confirm_registration(registration_id):
        """
        Confirm a registration
        
        Args:
            registration_id: Registration ID
        
        Returns:
            Number of affected rows
        """
        return Registration.update_registration_status(registration_id, 'confirmed')
    
    @staticmethod
    def get_registration_by_user_event(user_id, event_id):
        """
        Get registration by user and event
        
        Args:
            user_id: User ID
            event_id: Event ID
        
        Returns:
            Registration dictionary or None
        """
        query = """
            SELECT * FROM registrations 
            WHERE user_id = %s AND event_id = %s
        """
        return execute_one(query, (user_id, event_id))
    
    @staticmethod
    def get_confirmed_registrations_count(event_id):
        """
        Get count of confirmed registrations for an event
        
        Args:
            event_id: Event ID
        
        Returns:
            Count of confirmed registrations
        """
        query = """
            SELECT COUNT(*) as count 
            FROM registrations 
            WHERE event_id = %s AND status = 'confirmed'
        """
        result = execute_one(query, (event_id,))
        return result['count'] if result else 0
    
    @staticmethod
    def delete_registration(registration_id):
        """
        Delete a registration
        
        Args:
            registration_id: Registration ID
        
        Returns:
            Number of affected rows
        """
        query = "DELETE FROM registrations WHERE registration_id = %s"
        return execute_query(query, (registration_id,))
