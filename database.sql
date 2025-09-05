-- Travel Tour Database Schema (phpMyAdmin-friendly)

-- (Optional) Create & use database
CREATE DATABASE IF NOT EXISTS travel_tour_db;
USE travel_tour_db;

-- Drop tables in FK-safe order
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS traveler_details;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS travel_services;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS admins;

-- Admins
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    customername VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Customers (no CHECK here; we’ll use triggers)
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Travel Services
CREATE TABLE travel_services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10,2) NOT NULL,
    rating DECIMAL(2,1),
    destination VARCHAR(100),
    service_type ENUM('flight','hotel','tour') NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bookings
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    travel_date DATE NOT NULL,
    num_travelers INT DEFAULT 1,
    status ENUM('pending','confirmed','canceled') DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    CONSTRAINT fk_bookings_customer
      FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_bookings_service
      FOREIGN KEY (service_id) REFERENCES travel_services(service_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Traveler Details
CREATE TABLE traveler_details (
    traveler_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    gender ENUM('male','female','other'),
    dob DATE,
    passport_number VARCHAR(50),
    CONSTRAINT fk_travelers_booking
      FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Payments
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method ENUM('credit_card','e_wallet','gateway'),
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending','paid','failed') DEFAULT 'pending',
    transaction_ref VARCHAR(100) UNIQUE,
    CONSTRAINT fk_payments_booking
      FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Reviews (rating validated by triggers)
CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    rating INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reviews_customer
      FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_service
      FOREIGN KEY (service_id) REFERENCES travel_services(service_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ===========================
-- Validation Triggers
-- ===========================
DELIMITER $$

-- Customers.phone must be 10 digits starting with 0 (e.g., 0XXXXXXXXX)
CREATE TRIGGER trg_customers_phone_bi
BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
  IF NEW.phone IS NOT NULL AND NEW.phone NOT REGEXP '^[0][0-9]{9}$' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid phone: must be 10 digits starting with 0';
  END IF;
END$$

CREATE TRIGGER trg_customers_phone_bu
BEFORE UPDATE ON customers
FOR EACH ROW
BEGIN
  IF NEW.phone IS NOT NULL AND NEW.phone NOT REGEXP '^[0][0-9]{9}$' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid phone: must be 10 digits starting with 0';
  END IF;
END$$

-- Reviews.rating must be between 1 and 5
CREATE TRIGGER trg_reviews_rating_bi
BEFORE INSERT ON reviews
FOR EACH ROW
BEGIN
  IF NEW.rating IS NULL OR NEW.rating < 1 OR NEW.rating > 5 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid review rating: must be 1..5';
  END IF;
END$$

CREATE TRIGGER trg_reviews_rating_bu
BEFORE UPDATE ON reviews
FOR EACH ROW
BEGIN
  IF NEW.rating IS NULL OR NEW.rating < 1 OR NEW.rating > 5 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid review rating: must be 1..5';
  END IF;
END$$

DELIMITER ;
