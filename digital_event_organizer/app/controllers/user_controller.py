"""
User Controller
Handles user-related business logic
"""

from app.models.user import User
from app.models.registration import Registration
from app.utils.validators import validate_email, validate_password, validate_phone

class UserController:
    """Controller for user operations"""
    
    @staticmethod
    def register_user(name, email, password, phone):
        """
        Register a new user
        
        Args:
            name: User's full name
            email: User's email
            password: User's password
            phone: User's phone number
        
        Returns:
            Tuple: (success: Boolean, message: str, user_id: int or None)
        """
        # Validate inputs
        if not name or not name.strip():
            return False, "Name is required", None
        
        if not validate_email(email):
            return False, "Invalid email format", None
        
        valid_password, password_error = validate_password(password)
        if not valid_password:
            return False, password_error, None
        
        if not validate_phone(phone):
            return False, "Invalid phone number (should be 10 digits)", None
        
        # Check if email already exists
        if User.email_exists(email):
            return False, "Email already registered", None
        
        # Create user
        user_id = User.create_user(name.strip(), email, password, phone)
        
        if user_id:
            return True, "Registration successful", user_id
        else:
            return False, "Registration failed. Please try again.", None
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate user login
        
        Args:
            email: User's email
            password: User's password
        
        Returns:
            Tuple: (success: Boolean, message: str, user: dict or None)
        """
        if not email or not password:
            return False, "Email and password are required", None
        
        # Get user by email
        user = User.get_user_by_email(email)
        
        if not user:
            return False, "Invalid email or password", None
        
        # Verify password
        if not User.verify_password(user['password'], password):
            return False, "Invalid email or password", None
        
        # Remove password from user object before returning
        user.pop('password', None)
        
        return True, "Login successful", user
    
    @staticmethod
    def get_user_profile(user_id):
        """
        Get user profile information
        
        Args:
            user_id: User ID
        
        Returns:
            User dictionary without password
        """
        user = User.get_user_by_id(user_id)
        
        if user:
            user.pop('password', None)
            return user
        
        return None
    
    @staticmethod
    def update_user_profile(user_id, name=None, phone=None):
        """
        Update user profile
        
        Args:
            user_id: User ID
            name: New name (optional)
            phone: New phone (optional)
        
        Returns:
            Tuple: (success: Boolean, message: str)
        """
        if phone and not validate_phone(phone):
            return False, "Invalid phone number"
        
        affected = User.update_user(user_id, name, phone)
        
        if affected:
            return True, "Profile updated successfully"
        else:
            return False, "No changes made"
    
    @staticmethod
    def get_user_registrations(user_id):
        """
        Get all registrations for a user
        
        Args:
            user_id: User ID
        
        Returns:
            List of registrations with event details
        """
        return Registration.get_user_registrations(user_id)
