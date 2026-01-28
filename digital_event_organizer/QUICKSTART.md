# Quick Start Guide - Digital Event Organizer

## ⚡ 5-Minute Setup

### Step 1: Install Python & MySQL
- Download Python 3.8+ from python.org
- Download MySQL 8.0 from mysql.com
- Install both with default settings

### Step 2: Setup Project
```bash
# Extract the zip file
cd digital_event_organizer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Setup Database
```bash
# Login to MySQL
mysql -u root -p

# Import database
mysql -u root -p < database/schema.sql
```

### Step 4: Configure .env File
Edit the `.env` file:
```
DB_PASSWORD=your_mysql_password
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

### Step 5: Run Application
```bash
python run.py
```

Visit: http://localhost:5000

## 🔐 Default Login Credentials

**Admin:**
- Email: admin@eventorganizer.com
- Password: admin123

**User:**
- Email: john@example.com
- Password: user123

## 📧 Email Setup (Optional)

1. Go to myaccount.google.com
2. Security → 2-Step Verification → App Passwords
3. Generate password
4. Add to .env file as MAIL_PASSWORD

## 💳 Payment Setup (Optional)

1. Sign up at razorpay.com
2. Get test API keys
3. Add to .env:
   - RAZORPAY_KEY_ID
   - RAZORPAY_KEY_SECRET

## ✅ Testing Checklist

- [ ] Database created successfully
- [ ] Application runs on localhost:5000
- [ ] Can login as user
- [ ] Can login as admin
- [ ] Can view events
- [ ] Can register for free event
- [ ] Can create event (admin)

## 🐛 Common Issues

**Error: No module named 'flask'**
→ Activate virtual environment

**Error: Access denied for user**
→ Check DB_PASSWORD in .env

**Error: Can't connect to MySQL**
→ Start MySQL service

## 📱 Features to Demo

1. User registration and login
2. Browse events with search/filter
3. Register for free event
4. Admin dashboard with statistics
5. Create new event as admin
6. View participants list
7. Payment flow (test mode)

## 📚 Project Structure

```
app/
├── models/          → Database operations
├── controllers/     → Business logic
├── routes/          → URL routing
├── templates/       → HTML files
├── static/          → CSS, JS, images
└── utils/           → Helper functions
```

## 🎯 For College Viva

**Be ready to explain:**
1. MVC architecture
2. Database schema and relationships
3. Flask blueprints and routing
4. Payment integration (Razorpay)
5. Email notifications (Flask-Mail)
6. Security (password hashing, SQL injection prevention)

## 📊 Sample Data

The database comes with:
- 1 Admin user
- 3 Sample users
- 5 Sample events
- 3 Sample registrations

## 🚀 Next Steps

1. Test all features thoroughly
2. Add your own events
3. Customize templates if needed
4. Prepare project report
5. Practice explaining code for viva

## 💡 Tips

- Keep localhost:5000 open during demo
- Have MySQL running in background
- Test email notifications beforehand
- Practice payment flow multiple times
- Keep test cards ready for Razorpay

## 📞 Support

If you encounter issues:
1. Check README.md for detailed docs
2. Verify all dependencies installed
3. Check MySQL is running
4. Ensure .env file is configured

Good luck with your project! 🎓
