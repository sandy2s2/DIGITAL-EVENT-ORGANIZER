# Digital Event Organizer

A complete web-based event management system built with Flask, MySQL, and Bootstrap for college project submission.

## Features

### User Features
- User registration and login
- Browse upcoming events
- Search and filter events by category
- View event details
- Register for free and paid events
- View registration history
- Profile management
- Email notifications

### Admin Features
- Admin login with separate dashboard
- Create, update, and delete events
- View all registered participants
- Manage event categories
- View payment reports
- Dashboard with statistics

### Payment Integration
- Razorpay payment gateway (test mode)
- Secure payment processing
- Payment verification
- Transaction history

## Technology Stack

- **Backend:** Python 3.8+, Flask 2.3.0
- **Database:** MySQL 8.0
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Email:** Flask-Mail (SMTP)
- **Payment:** Razorpay SDK

## Project Structure

```
digital_event_organizer/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── controllers/             # Business logic
│   ├── models/                  # Database models
│   ├── routes/                  # URL routes (blueprints)
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── user/               # User templates
│   │   └── admin/              # Admin templates
│   ├── static/                  # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/                   # Utility functions
├── database/
│   └── schema.sql               # Database schema
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env                         # Environment variables
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
# If using git
git clone <repository-url>
cd digital_event_organizer

# Or extract the zip file
unzip digital_event_organizer.zip
cd digital_event_organizer
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Create database and import schema
mysql -u root -p < database/schema.sql
```

### Step 5: Configure Environment Variables
Edit `.env` file with your settings:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=digital_event_organizer

# Flask Secret Key
SECRET_KEY=your-secret-key-here

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Razorpay (Test Mode)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

### Step 6: Run the Application
```bash
python run.py
```

The application will start at `http://localhost:5000`

## Default Credentials

### Admin Login
- Email: `admin@eventorganizer.com`
- Password: `admin123`

### Test User Login
- Email: `john@example.com`
- Password: `user123`

## Usage Guide

### For Users
1. Register for a new account
2. Login with your credentials
3. Browse events on the Events page
4. Click on an event to view details
5. Click "Register Now" to register
6. For paid events, complete payment
7. View your registrations in "My Registrations"

### For Admins
1. Login with admin credentials
2. View dashboard statistics
3. Create new events using "Create Event" button
4. Manage existing events from "Manage Events"
5. View participants for each event
6. Edit or delete events as needed

## Email Configuration

### Using Gmail SMTP
1. Enable 2-factor authentication in your Google account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security > 2-Step Verification
   - App passwords > Generate
3. Use the generated password in `.env` file

## Payment Gateway Setup

### Razorpay Test Mode
1. Sign up at https://razorpay.com
2. Get your test API keys from Dashboard
3. Add keys to `.env` file
4. Use test cards for testing payments

## Database Schema

### Tables
1. **users** - User and admin information
2. **events** - Event details
3. **registrations** - Event registrations
4. **payments** - Payment transactions
5. **notifications** - Email notifications (optional)

## API Endpoints

### User Routes
- `POST /user/register` - User registration
- `POST /user/login` - User login
- `GET /user/dashboard` - User dashboard
- `GET /user/events` - Browse events
- `POST /user/events/<id>/register` - Register for event

### Admin Routes
- `POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard
- `POST /admin/events/create` - Create event
- `PUT /admin/events/<id>/edit` - Update event
- `DELETE /admin/events/<id>/delete` - Delete event

## Testing

### Test Cases
1. **User Registration** - Register with valid details
2. **User Login** - Login with credentials
3. **Browse Events** - View all events
4. **Event Registration (Free)** - Register for free event
5. **Event Registration (Paid)** - Complete payment flow
6. **Admin Login** - Login as admin
7. **Create Event** - Admin creates new event
8. **View Participants** - Admin views registrations

## Troubleshooting

### Common Issues

**Issue:** Database connection error
**Solution:** Check MySQL is running and credentials in `.env` are correct

**Issue:** Email not sending
**Solution:** Verify Gmail App Password and SMTP settings

**Issue:** Payment gateway error
**Solution:** Check Razorpay API keys and test mode is enabled

**Issue:** Module not found error
**Solution:** Make sure virtual environment is activated and dependencies are installed

## Deployment

### For College Demo
- Run locally on `localhost:5000`
- Use test database with sample data
- Enable debug mode for easier troubleshooting

### For Production (Optional)
1. Set `DEBUG=False` in `.env`
2. Use strong `SECRET_KEY`
3. Use production database
4. Deploy on:
   - PythonAnywhere (free tier)
   - Heroku
   - AWS/Google Cloud
   - College server

## Project Report Sections

### For College Submission
1. **Abstract** - Brief overview of the project
2. **Introduction** - Problem statement and objectives
3. **Literature Survey** - Related work and technologies
4. **System Analysis** - Requirements and feasibility
5. **System Design** - Architecture and ER diagrams
6. **Implementation** - Code snippets and screenshots
7. **Testing** - Test cases and results
8. **Conclusion** - Summary and future enhancements
9. **References** - Books, websites, documentation

## Viva Preparation

### Expected Questions

**1. Why Flask over Django?**
- Lightweight and flexible
- Easier to learn
- Better for small-medium projects
- More control over components

**2. Explain MVC pattern**
- Model: Database operations (models/)
- View: HTML templates (templates/)
- Controller: Business logic (controllers/)

**3. How is payment security handled?**
- Using test/sandbox mode only
- No storage of card details
- Payment gateway handles encryption
- Signature verification for transactions

**4. How are passwords stored?**
- Hashed using werkzeug.security
- Never stored in plain text
- bcrypt algorithm for hashing

**5. Explain the database relationships**
- Users → Registrations (One-to-Many)
- Events → Registrations (One-to-Many)
- Registrations → Payments (One-to-One)

## Future Enhancements

1. QR code tickets
2. Google Calendar integration
3. Social media sharing
4. Event reviews and ratings
5. Analytics dashboard
6. Mobile app (React Native)
7. Real-time chat support
8. Multi-language support

## License

This project is for educational purposes only.

## Contact

For queries related to this project:
- Create an issue in the repository
- Contact your project guide

## Acknowledgments

- Flask Documentation
- Bootstrap Documentation
- Razorpay API Documentation
- MySQL Documentation

---

**Note:** This is an academic project. Please ensure you follow your college's guidelines for project submission.
