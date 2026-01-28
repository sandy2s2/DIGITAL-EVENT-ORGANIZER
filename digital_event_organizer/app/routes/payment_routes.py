"""
Payment Routes
Handles payment-related HTTP routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from app.controllers.payment_controller import PaymentController
from functools import wraps

# Create Blueprint
payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

@payment_bp.route('/initiate/<int:registration_id>')
@login_required
def initiate(registration_id):
    """Initiate payment for a registration"""
    user_id = session.get('user_id')
    
    # Create payment order
    success, message, order_data = PaymentController.initiate_payment(registration_id, user_id)
    
    if not success:
        flash(message, 'danger')
        return redirect(url_for('user.my_registrations'))
    
    # Get Razorpay key from config
    razorpay_key = current_app.config.get('RAZORPAY_KEY_ID')
    
    return render_template('user/payment.html', 
                         order_data=order_data,
                         razorpay_key=razorpay_key,
                         user_name=session.get('user_name'),
                         user_email=session.get('user_email'))

@payment_bp.route('/verify', methods=['POST'])
@login_required
def verify():
    """Verify payment after completion"""
    # Get payment details from request
    payment_id = request.form.get('payment_id')
    razorpay_order_id = request.form.get('razorpay_order_id')
    razorpay_payment_id = request.form.get('razorpay_payment_id')
    razorpay_signature = request.form.get('razorpay_signature')
    
    # Verify and complete payment
    success, message = PaymentController.verify_and_complete_payment(
        payment_id=payment_id,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature
    )
    
    if success:
        flash(message, 'success')
        return redirect(url_for('user.my_registrations'))
    else:
        flash(message, 'danger')
        return redirect(url_for('user.my_registrations'))

@payment_bp.route('/failure', methods=['POST'])
@login_required
def failure():
    """Handle payment failure"""
    payment_id = request.form.get('payment_id')
    
    if payment_id:
        PaymentController.handle_payment_failure(payment_id)
    
    flash('Payment failed. Please try again.', 'danger')
    return redirect(url_for('user.my_registrations'))

@payment_bp.route('/success')
@login_required
def success():
    """Payment success page"""
    flash('Payment successful! Your registration is confirmed.', 'success')
    return redirect(url_for('user.my_registrations'))

@payment_bp.route('/history')
@login_required
def payment_history():
    """View payment history"""
    user_id = session.get('user_id')
    payments = PaymentController.get_user_payments(user_id)
    
    return render_template('user/payment_history.html', payments=payments)
