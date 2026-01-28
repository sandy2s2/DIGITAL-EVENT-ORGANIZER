"""
Admin Controller
Handles admin-related business logic
"""

from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration
from app.models.payment import Payment

class AdminController:
    """Controller for admin operations"""
    
    @staticmethod
    def admin_login(email, password):
        """
        Authenticate admin login
        
        Args:
            email: Admin's email
            password: Admin's password
        
        Returns:
            Tuple: (success: Boolean, message: str, admin: dict or None)
        """
        if not email or not password:
            return False, "Email and password are required", None
        
        # Get user by email
        user = User.get_user_by_email(email)
        
        if not user:
            return False, "Invalid email or password", None
        
        # Check if user is admin
        if user['role'] != 'admin':
            return False, "Access denied. Admin privileges required.", None
        
        # Verify password
        if not User.verify_password(user['password'], password):
            return False, "Invalid email or password", None
        
        # Remove password from user object
        user.pop('password', None)
        
        return True, "Admin login successful", user
    
    @staticmethod
    def get_dashboard_stats():
        """
        Get dashboard statistics for admin
        
        Returns:
            Dictionary with statistics
        """
        all_events = Event.get_all_events() or []
        upcoming_events = Event.get_upcoming_events() or []
        all_users = User.get_all_users() or []
        
        stats = {
            'total_events': len(all_events),
            'upcoming_events': len(upcoming_events),
            'total_users': len(all_users),
            'total_registrations': 0,
            'total_revenue': 0.0
        }
        
        # Calculate total registrations and revenue
        for event in all_events:
            event_id = event['event_id']
            stats['total_registrations'] += Registration.get_confirmed_registrations_count(event_id)
            stats['total_revenue'] += Payment.get_total_revenue(event_id)
        
        return stats
    
    @staticmethod
    def get_all_events():
        """
        Get all events for admin
        
        Returns:
            List of events
        """
        return Event.get_all_events()
    
    @staticmethod
    def get_event_participants(event_id):
        """
        Get all participants for an event
        
        Args:
            event_id: Event ID
        
        Returns:
            List of participants with registration details
        """
        return Registration.get_event_registrations(event_id)
    
    @staticmethod
    def get_event_payments(event_id):
        """
        Get all payments for an event
        
        Args:
            event_id: Event ID
        
        Returns:
            List of payments
        """
        return Payment.get_event_payments(event_id)
    
    @staticmethod
    def get_all_users():
        """
        Get all users
        
        Returns:
            List of users
        """
        return User.get_all_users()
