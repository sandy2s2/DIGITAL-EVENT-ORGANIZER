"""
Payment Controller
Handles payment-related business logic
"""

from app.models.payment import Payment
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User
from app.utils.payment_service import create_order, verify_payment_signature
from app.utils.email_service import send_payment_confirmation, send_registration_confirmation

class PaymentController:
    """Controller for payment operations"""
    
    @staticmethod
    def initiate_payment(registration_id, user_id):
        """
        Initiate payment for a registration
        
        Args:
            registration_id: Registration ID
            user_id: User ID
        
        Returns:
            Tuple: (success: Boolean, message: str, order_data: dict or None)
        """
        # Get registration details
        registration = Registration.get_registration_by_id(registration_id)
        
        if not registration:
            return False, "Registration not found", None
        
        if registration['user_id'] != user_id:
            return False, "Unauthorized access", None
        
        # Get event details
        event = Event.get_event_by_id(registration['event_id'])
        
        if not event:
            return False, "Event not found", None
        
        if not event['is_paid']:
            return False, "This is a free event", None
        
        # Check if payment already exists
        existing_payment = Payment.get_payment_by_registration(registration_id)
        if existing_payment and existing_payment['payment_status'] == 'success':
            return False, "Payment already completed", None
        
        # Create Razorpay order
        amount = float(event['price'])
        receipt = f"reg_{registration_id}"
        
        order = create_order(amount, receipt=receipt)
        
        if not order:
            return False, "Failed to create payment order", None
        
        # Create payment record
        payment_id = Payment.create_payment(
            registration_id=registration_id,
            user_id=user_id,
            event_id=event['event_id'],
            amount=amount,
            transaction_id=order['id'],
            payment_method='razorpay'
        )
        
        if not payment_id:
            return False, "Failed to create payment record", None
        
        # Return order data for frontend
        order_data = {
            'order_id': order['id'],
            'amount': order['amount'],  # Amount in paise
            'currency': order['currency'],
            'payment_id': payment_id,
            'event_title': event['title']
        }
        
        return True, "Payment order created", order_data
    
    @staticmethod
    def verify_and_complete_payment(payment_id, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verify payment signature and complete payment
        
        Args:
            payment_id: Payment ID from database
            razorpay_order_id: Razorpay order ID
            razorpay_payment_id: Razorpay payment ID
            razorpay_signature: Razorpay signature
        
        Returns:
            Tuple: (success: Boolean, message: str)
        """
        # Verify signature
        is_valid = verify_payment_signature(
            order_id=razorpay_order_id,
            payment_id=razorpay_payment_id,
            signature=razorpay_signature
        )
        
        if not is_valid:
            # Mark payment as failed
            Payment.mark_payment_failed(payment_id)
            return False, "Payment verification failed"
        
        # Get payment details
        payment = Payment.get_payment_by_id(payment_id)
        
        if not payment:
            return False, "Payment record not found"
        
        # Mark payment as successful
        Payment.mark_payment_success(payment_id, razorpay_payment_id)
        
        # Confirm registration
        Registration.confirm_registration(payment['registration_id'])
        
        # Get user and event details for email
        user = User.get_user_by_id(payment['user_id'])
        event = Event.get_event_by_id(payment['event_id'])
        
        if user and event:
            # Send payment confirmation email
            send_payment_confirmation(
                user_email=user['email'],
                user_name=user['name'],
                event_title=event['title'],
                amount=payment['amount'],
                transaction_id=razorpay_payment_id
            )
            
            # Send registration confirmation email
            send_registration_confirmation(
                user_email=user['email'],
                user_name=user['name'],
                event_title=event['title'],
                event_date=str(event['event_date']),
                event_time=str(event['event_time']),
                venue=event['venue']
            )
        
        return True, "Payment successful! Registration confirmed."
    
    @staticmethod
    def handle_payment_failure(payment_id):
        """
        Handle payment failure
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Tuple: (success: Boolean, message: str)
        """
        # Mark payment as failed
        affected = Payment.mark_payment_failed(payment_id)
        
        if affected:
            return True, "Payment marked as failed"
        else:
            return False, "Failed to update payment status"
    
    @staticmethod
    def get_user_payments(user_id):
        """
        Get all payments for a user
        
        Args:
            user_id: User ID
        
        Returns:
            List of payments
        """
        return Payment.get_user_payments(user_id)
    
    @staticmethod
    def get_payment_details(payment_id, user_id):
        """
        Get payment details
        
        Args:
            payment_id: Payment ID
            user_id: User ID (for authorization)
        
        Returns:
            Payment dictionary or None
        """
        payment = Payment.get_payment_by_id(payment_id)
        
        if payment and payment['user_id'] == user_id:
            return payment
        
        return None
