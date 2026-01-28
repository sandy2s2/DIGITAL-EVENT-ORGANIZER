"""
Payment Model
Handles all payment-related database operations
"""

from app.utils.db_config import execute_query, execute_one

class Payment:
    """Payment model for database operations"""
    
    @staticmethod
    def create_payment(registration_id, user_id, event_id, amount, transaction_id=None, payment_method='razorpay'):
        """
        Create a new payment record
        
        Args:
            registration_id: Registration ID
            user_id: User ID
            event_id: Event ID
            amount: Payment amount
            transaction_id: Payment gateway transaction ID
            payment_method: Payment method (default 'razorpay')
        
        Returns:
            payment_id if successful, None otherwise
        """
        query = """
            INSERT INTO payments 
            (registration_id, user_id, event_id, amount, transaction_id, 
             payment_method, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (registration_id, user_id, event_id, amount, transaction_id, 
                 payment_method, 'pending')
        
        return execute_query(query, params)
    
    @staticmethod
    def get_payment_by_id(payment_id):
        """
        Get payment by ID
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Payment dictionary or None
        """
        query = "SELECT * FROM payments WHERE payment_id = %s"
        return execute_one(query, (payment_id,))
    
    @staticmethod
    def get_payment_by_transaction_id(transaction_id):
        """
        Get payment by transaction ID
        
        Args:
            transaction_id: Payment gateway transaction ID
        
        Returns:
            Payment dictionary or None
        """
        query = "SELECT * FROM payments WHERE transaction_id = %s"
        return execute_one(query, (transaction_id,))
    
    @staticmethod
    def get_payment_by_registration(registration_id):
        """
        Get payment for a registration
        
        Args:
            registration_id: Registration ID
        
        Returns:
            Payment dictionary or None
        """
        query = "SELECT * FROM payments WHERE registration_id = %s"
        return execute_one(query, (registration_id,))
    
    @staticmethod
    def get_user_payments(user_id):
        """
        Get all payments for a user with event details
        
        Args:
            user_id: User ID
        
        Returns:
            List of payment dictionaries with event details
        """
        query = """
            SELECT p.*, e.title, e.event_date, e.event_time
            FROM payments p
            JOIN events e ON p.event_id = e.event_id
            WHERE p.user_id = %s
            ORDER BY p.payment_date DESC
        """
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_event_payments(event_id):
        """
        Get all payments for an event
        
        Args:
            event_id: Event ID
        
        Returns:
            List of payment dictionaries with user details
        """
        query = """
            SELECT p.*, u.name, u.email
            FROM payments p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.event_id = %s
            ORDER BY p.payment_date DESC
        """
        return execute_query(query, (event_id,), fetch=True)
    
    @staticmethod
    def update_payment_status(payment_id, status, transaction_id=None):
        """
        Update payment status
        
        Args:
            payment_id: Payment ID
            status: New status ('pending', 'success', 'failed', 'refunded')
            transaction_id: Transaction ID (optional)
        
        Returns:
            Number of affected rows
        """
        if transaction_id:
            query = """
                UPDATE payments 
                SET payment_status = %s, transaction_id = %s 
                WHERE payment_id = %s
            """
            params = (status, transaction_id, payment_id)
        else:
            query = "UPDATE payments SET payment_status = %s WHERE payment_id = %s"
            params = (status, payment_id)
        
        return execute_query(query, params)
    
    @staticmethod
    def mark_payment_success(payment_id, transaction_id):
        """
        Mark payment as successful
        
        Args:
            payment_id: Payment ID
            transaction_id: Payment gateway transaction ID
        
        Returns:
            Number of affected rows
        """
        return Payment.update_payment_status(payment_id, 'success', transaction_id)
    
    @staticmethod
    def mark_payment_failed(payment_id):
        """
        Mark payment as failed
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Number of affected rows
        """
        return Payment.update_payment_status(payment_id, 'failed')
    
    @staticmethod
    def get_successful_payments_count(event_id):
        """
        Get count of successful payments for an event
        
        Args:
            event_id: Event ID
        
        Returns:
            Count of successful payments
        """
        query = """
            SELECT COUNT(*) as count 
            FROM payments 
            WHERE event_id = %s AND payment_status = 'success'
        """
        result = execute_one(query, (event_id,))
        return result['count'] if result else 0
    
    @staticmethod
    def get_total_revenue(event_id):
        """
        Get total revenue for an event
        
        Args:
            event_id: Event ID
        
        Returns:
            Total revenue amount
        """
        query = """
            SELECT SUM(amount) as total 
            FROM payments 
            WHERE event_id = %s AND payment_status = 'success'
        """
        result = execute_one(query, (event_id,))
        return float(result['total']) if result and result['total'] else 0.0
