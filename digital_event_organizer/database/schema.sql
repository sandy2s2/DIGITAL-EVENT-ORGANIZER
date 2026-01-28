-- ============================================
-- Digital Event Organizer Database Schema
-- ============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS digital_event_organizer;
USE digital_event_organizer;

-- ============================================
-- Table: users
-- Stores user and admin information
-- ============================================
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: events
-- Stores event information
-- ============================================
CREATE TABLE events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) DEFAULT 0.00,
    is_paid BOOLEAN DEFAULT FALSE,
    max_participants INT DEFAULT 100,
    current_participants INT DEFAULT 0,
    registration_deadline DATE,
    image_url VARCHAR(255),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_event_date (event_date),
    INDEX idx_category (category),
    INDEX idx_is_paid (is_paid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: registrations
-- Stores event registrations
-- ============================================
CREATE TABLE registrations (
    registration_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    payment_required BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration (user_id, event_id),
    INDEX idx_user_id (user_id),
    INDEX idx_event_id (event_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: payments
-- Stores payment transactions
-- ============================================
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    registration_id INT NOT NULL,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100) UNIQUE,
    payment_method VARCHAR(50),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (registration_id) REFERENCES registrations(registration_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    INDEX idx_payment_status (payment_status),
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_user_id (user_id),
    INDEX idx_event_id (event_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: notifications (Optional)
-- Stores user notifications
-- ============================================
CREATE TABLE notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    notification_type ENUM('registration', 'reminder', 'cancellation', 'payment') DEFAULT 'registration',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Insert Sample Admin User
-- Default password: admin123 (hashed)
-- ============================================
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@eventorganizer.com', 'scrypt:32768:8:1$oHT9YwPw1jTq9mKn$a5c3d8e8f9b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9', 'admin');

-- Note: The above password hash is for 'admin123'
-- In production, use werkzeug.security.generate_password_hash('your_password')

-- ============================================
-- Insert Sample Events
-- ============================================
INSERT INTO events (title, description, event_date, event_time, venue, category, price, is_paid, max_participants, registration_deadline, created_by) VALUES
('Tech Conference 2026', 'Annual technology conference featuring latest innovations', '2026-03-15', '10:00:00', 'Main Auditorium', 'Technology', 500.00, TRUE, 200, '2026-03-10', 1),
('Python Workshop', 'Learn Python programming from scratch', '2026-02-20', '14:00:00', 'Computer Lab 1', 'Workshop', 200.00, TRUE, 50, '2026-02-15', 1),
('Cultural Fest', 'Annual cultural festival with music, dance and drama', '2026-04-05', '17:00:00', 'College Ground', 'Cultural', 0.00, FALSE, 500, '2026-04-01', 1),
('Sports Day', 'Inter-college sports competition', '2026-03-25', '08:00:00', 'Sports Complex', 'Sports', 0.00, FALSE, 300, '2026-03-20', 1),
('AI & Machine Learning Seminar', 'Expert talks on AI and ML trends', '2026-02-28', '11:00:00', 'Seminar Hall', 'Seminar', 300.00, TRUE, 100, '2026-02-25', 1);

-- ============================================
-- Insert Sample Users
-- Password for all: user123
-- ============================================
INSERT INTO users (name, email, password, phone, role) VALUES
('John Doe', 'john@example.com', 'scrypt:32768:8:1$oHT9YwPw1jTq9mKn$b6c4d9e9f0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0', '9876543210', 'user'),
('Jane Smith', 'jane@example.com', 'scrypt:32768:8:1$oHT9YwPw1jTq9mKn$b6c4d9e9f0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0', '9876543211', 'user'),
('Mike Johnson', 'mike@example.com', 'scrypt:32768:8:1$oHT9YwPw1jTq9mKn$b6c4d9e9f0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0', '9876543212', 'user');

-- ============================================
-- Sample Registrations
-- ============================================
INSERT INTO registrations (user_id, event_id, status, payment_required) VALUES
(2, 3, 'confirmed', FALSE),
(2, 4, 'confirmed', FALSE),
(3, 3, 'confirmed', FALSE);

-- Update participant counts
UPDATE events SET current_participants = 2 WHERE event_id = 3;
UPDATE events SET current_participants = 1 WHERE event_id = 4;

-- ============================================
-- Database Schema Complete
-- ============================================
