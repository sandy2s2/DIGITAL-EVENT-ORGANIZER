"""
Input Validation Module
Validates user inputs to prevent security issues
"""

import re
from datetime import datetime

def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        Boolean: True if valid email format
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """
    Validate phone number (10 digits)
    
    Args:
        phone: Phone number string
    
    Returns:
        Boolean: True if valid phone number
    """
    if not phone:
        return False
    
    # Remove spaces and special characters
    phone = re.sub(r'[^0-9]', '', phone)
    
    # Check if 10 digits
    return len(phone) == 10

def validate_password(password):
    """
    Validate password strength
    Minimum 6 characters
    
    Args:
        password: Password string
    
    Returns:
        Tuple: (Boolean, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, ""

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present and not empty
    
    Args:
        data: Dictionary of form data
        required_fields: List of required field names
    
    Returns:
        Tuple: (Boolean, missing_fields list)
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            missing_fields.append(field)
    
    return len(missing_fields) == 0, missing_fields

def validate_date(date_string, format='%Y-%m-%d'):
    """
    Validate date string format
    
    Args:
        date_string: Date as string
        format: Expected date format
    
    Returns:
        Boolean: True if valid date
    """
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False

def validate_time(time_string, format='%H:%M'):
    """
    Validate time string format
    
    Args:
        time_string: Time as string
        format: Expected time format
    
    Returns:
        Boolean: True if valid time
    """
    try:
        datetime.strptime(time_string, format)
        return True
    except ValueError:
        return False

def sanitize_input(input_string):
    """
    Sanitize input to prevent XSS attacks
    
    Args:
        input_string: User input string
    
    Returns:
        Sanitized string
    """
    if not input_string:
        return ""
    
    # Remove HTML tags
    clean = re.sub(r'<[^>]*>', '', str(input_string))
    
    # Remove script tags content
    clean = re.sub(r'<script.*?</script>', '', clean, flags=re.DOTALL)
    
    return clean.strip()
