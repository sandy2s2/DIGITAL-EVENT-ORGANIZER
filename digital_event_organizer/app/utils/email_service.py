"""
Email Service Module
Handles sending emails for notifications and confirmations
"""

from flask_mail import Message
from app import mail
from flask import current_app

def send_email(to_email, subject, body):
    """
    Send an email using Flask-Mail
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (HTML supported)
    
    Returns:
        Boolean: True if sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_registration_confirmation(user_email, user_name, event_title, event_date, event_time, venue):
    """
    Send registration confirmation email
    """
    subject = f"Registration Confirmed - {event_title}"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Registration Confirmed!</h2>
            <p>Dear {user_name},</p>
            <p>Your registration for the following event has been confirmed:</p>
            
            <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px;">
                <h3 style="color: #333;">{event_title}</h3>
                <p><strong>Date:</strong> {event_date}</p>
                <p><strong>Time:</strong> {event_time}</p>
                <p><strong>Venue:</strong> {venue}</p>
            </div>
            
            <p>We look forward to seeing you at the event!</p>
            <p>Best regards,<br>Event Organizer Team</p>
        </body>
    </html>
    """
    return send_email(user_email, subject, body)

def send_payment_confirmation(user_email, user_name, event_title, amount, transaction_id):
    """
    Send payment confirmation email
    """
    subject = f"Payment Successful - {event_title}"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Payment Confirmed!</h2>
            <p>Dear {user_name},</p>
            <p>Your payment has been successfully processed.</p>
            
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px;">
                <p><strong>Event:</strong> {event_title}</p>
                <p><strong>Amount Paid:</strong> ₹{amount}</p>
                <p><strong>Transaction ID:</strong> {transaction_id}</p>
            </div>
            
            <p>Your registration is now confirmed!</p>
            <p>Best regards,<br>Event Organizer Team</p>
        </body>
    </html>
    """
    return send_email(user_email, subject, body)

def send_event_reminder(user_email, user_name, event_title, event_date, event_time, venue):
    """
    Send event reminder email (1 day before event)
    """
    subject = f"Reminder: {event_title} Tomorrow!"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Event Reminder</h2>
            <p>Dear {user_name},</p>
            <p>This is a friendly reminder about your upcoming event tomorrow:</p>
            
            <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px;">
                <h3 style="color: #333;">{event_title}</h3>
                <p><strong>Date:</strong> {event_date}</p>
                <p><strong>Time:</strong> {event_time}</p>
                <p><strong>Venue:</strong> {venue}</p>
            </div>
            
            <p>Don't forget to attend!</p>
            <p>Best regards,<br>Event Organizer Team</p>
        </body>
    </html>
    """
    return send_email(user_email, subject, body)

def send_event_cancellation(user_email, user_name, event_title):
    """
    Send event cancellation email
    """
    subject = f"Event Cancelled - {event_title}"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Event Cancellation Notice</h2>
            <p>Dear {user_name},</p>
            <p>We regret to inform you that the following event has been cancelled:</p>
            
            <div style="background-color: #ffebee; padding: 15px; border-radius: 5px;">
                <h3 style="color: #333;">{event_title}</h3>
            </div>
            
            <p>We apologize for any inconvenience caused. If you made any payment, it will be refunded within 7 business days.</p>
            <p>Best regards,<br>Event Organizer Team</p>
        </body>
    </html>
    """
    return send_email(user_email, subject, body)
