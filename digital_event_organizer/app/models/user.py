"""
User Model
Handles all user-related database operations
"""

from app.utils.db_config import execute_query, execute_one
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """User model for database operations"""
    
    @staticmethod
    def create_user(name, email, password, phone, role='user'):
        """
        Create a new user
        
        Args:
            name: User's full name
            email: User's email
            password: Plain text password (will be hashed)
            phone: User's phone number
            role: User role ('user' or 'admin')
        
        Returns:
            user_id if successful, None otherwise
        """
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        query = """
            INSERT INTO users (name, email, password, phone, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (name, email, hashed_password, phone, role)
        
        return execute_query(query, params)
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        
        Args:
            email: User's email
        
        Returns:
            User dictionary or None
        """
        query = "SELECT * FROM users WHERE email = %s"
        return execute_one(query, (email,))
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id: User's ID
        
        Returns:
            User dictionary or None
        """
        query = "SELECT * FROM users WHERE user_id = %s"
        return execute_one(query, (user_id,))
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        Verify if provided password matches stored hashed password
        
        Args:
            stored_password: Hashed password from database
            provided_password: Plain text password provided by user
        
        Returns:
            Boolean: True if passwords match
        """
        return check_password_hash(stored_password, provided_password)
    
    @staticmethod
    def update_user(user_id, name=None, phone=None):
        """
        Update user information
        
        Args:
            user_id: User's ID
            name: New name (optional)
            phone: New phone (optional)
        
        Returns:
            Number of affected rows
        """
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        
        if phone:
            updates.append("phone = %s")
            params.append(phone)
        
        if not updates:
            return 0
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        
        return execute_query(query, tuple(params))
    
    @staticmethod
    def get_all_users():
        """
        Get all users
        
        Returns:
            List of user dictionaries
        """
        query = "SELECT user_id, name, email, phone, role, created_at FROM users ORDER BY created_at DESC"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def email_exists(email):
        """
        Check if email already exists
        
        Args:
            email: Email to check
        
        Returns:
            Boolean: True if email exists
        """
        query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
        result = execute_one(query, (email,))
        return result and result['count'] > 0
