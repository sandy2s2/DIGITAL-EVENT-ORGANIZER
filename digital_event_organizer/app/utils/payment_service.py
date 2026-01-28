"""
Payment Service Module
Handles Razorpay payment gateway integration
"""

import razorpay
from flask import current_app
import hashlib
import hmac

def get_razorpay_client():
    """
    Create and return Razorpay client
    """
    return razorpay.Client(
        auth=(
            current_app.config['RAZORPAY_KEY_ID'],
            current_app.config['RAZORPAY_KEY_SECRET']
        )
    )

def create_order(amount, currency='INR', receipt=None):
    """
    Create a Razorpay order
    
    Args:
        amount: Amount in paise (multiply rupees by 100)
        currency: Currency code (default INR)
        receipt: Custom receipt ID
    
    Returns:
        Order object with order_id
    """
    try:
        client = get_razorpay_client()
        
        # Convert amount to paise (smallest currency unit)
        amount_in_paise = int(float(amount) * 100)
        
        order_data = {
            'amount': amount_in_paise,
            'currency': currency,
            'receipt': receipt or f'order_{amount_in_paise}',
            'payment_capture': 1  # Auto capture payment
        }
        
        order = client.order.create(data=order_data)
        return order
    
    except Exception as e:
        print(f"Error creating Razorpay order: {e}")
        return None

def verify_payment_signature(order_id, payment_id, signature):
    """
    Verify Razorpay payment signature
    
    Args:
        order_id: Razorpay order ID
        payment_id: Razorpay payment ID
        signature: Razorpay signature
    
    Returns:
        Boolean: True if signature is valid
    """
    try:
        client = get_razorpay_client()
        
        # Create expected signature
        message = f"{order_id}|{payment_id}"
        secret = current_app.config['RAZORPAY_KEY_SECRET']
        
        generated_signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return generated_signature == signature
    
    except Exception as e:
        print(f"Error verifying payment signature: {e}")
        return False

def fetch_payment_details(payment_id):
    """
    Fetch payment details from Razorpay
    
    Args:
        payment_id: Razorpay payment ID
    
    Returns:
        Payment object
    """
    try:
        client = get_razorpay_client()
        payment = client.payment.fetch(payment_id)
        return payment
    
    except Exception as e:
        print(f"Error fetching payment details: {e}")
        return None
