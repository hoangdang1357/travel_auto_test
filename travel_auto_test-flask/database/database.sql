-- Ghi chú: Để kích hoạt các ràng buộc khóa ngoại, hãy chạy lệnh này sau khi kết nối:
PRAGMA foreign_keys = ON;

-- ===========================
-- Tạo Bảng
-- ===========================

-- Xóa các bảng theo thứ tự an toàn để tránh lỗi khóa ngoại
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS traveler_details;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS travel_services;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS admins;

-- Bảng Quản trị viên (Admins)
CREATE TABLE admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,    -- Đã đổi
    password_hash TEXT NOT NULL,          -- Đã đổi
    email TEXT UNIQUE NOT NULL            -- Đã đổi
);

-- Bảng Khách hàng (Customers)
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,              -- Đã đổi
    email TEXT UNIQUE NOT NULL,           -- Đã đổi
    password_hash TEXT NOT NULL,          -- Đã đổi
    phone TEXT,                           -- Đã đổi
    address TEXT
);

-- Bảng Dịch vụ Du lịch (Travel Services)
CREATE TABLE travel_services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    price NUMERIC NOT NULL,              
    rating NUMERIC,                      
    destination TEXT,                    
    flight TEXT,        -- Thông tin chuyến bay, NULL nếu không phải flight
    hotel TEXT,         -- Thông tin khách sạn, NULL nếu không phải hotel
    tour TEXT,          -- Thông tin tour, NULL nếu không phải tour
    max_travelers INT, 
    title TEXT NOT NULL,                  
    description TEXT,
    start_date DATE,                      
    end_date DATE,                        
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Đặt chỗ (Bookings)
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT NOT NULL,             -- Giữ nguyên
    service_id INT NOT NULL,              -- Giữ nguyên
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Giữ nguyên
    travel_date DATE NOT NULL,            -- Giữ nguyên
    num_travelers INT DEFAULT 1,          -- Giữ nguyên
    status TEXT CHECK(status IN ('pending','confirmed','canceled')) DEFAULT 'pending',
    total_amount NUMERIC not null,                 -- Giữ nguyên
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES travel_services(service_id) ON DELETE CASCADE
);

-- Bảng Chi tiết Hành khách (Traveler Details)
CREATE TABLE traveler_details (
    traveler_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INT NOT NULL,              -- Giữ nguyên
    full_name TEXT NOT NULL,              -- Đã đổi
    gender TEXT CHECK(gender IN ('male','female','other')),
    dob DATE,                             -- Giữ nguyên
    passport_number TEXT,                 -- Đã đổi
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- Bảng Thanh toán (Payments)
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INT NOT NULL,              -- Giữ nguyên
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Giữ nguyên
    payment_method TEXT CHECK(payment_method IN ('credit_card','e_wallet','gateway')),
    amount NUMERIC NOT NULL,              -- Giữ nguyên
    status TEXT CHECK(status IN ('pending','paid','failed')) DEFAULT 'pending',
    transaction_ref TEXT UNIQUE,          -- Đã đổi
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- Bảng Đánh giá (Reviews)
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT NOT NULL,             -- Giữ nguyên
    service_id INT NOT NULL,              -- Giữ nguyên
    rating INT,                           -- Giữ nguyên
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Giữ nguyên
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES travel_services(service_id) ON DELETE CASCADE
);

-- ===========================
-- Trigger xác thực dữ liệu
-- (Không cần thay đổi)
-- ===========================

CREATE TRIGGER trg_customers_phone_bi
BEFORE INSERT ON customers
FOR EACH ROW
WHEN NEW.phone IS NOT NULL AND (length(NEW.phone) != 10 OR substr(NEW.phone, 1, 1) != '0')
BEGIN
    SELECT RAISE(FAIL, 'Invalid phone: must be 10 digits starting with 0');
END;

CREATE TRIGGER trg_customers_phone_bu
BEFORE UPDATE ON customers
FOR EACH ROW
WHEN NEW.phone IS NOT NULL AND (length(NEW.phone) != 10 OR substr(NEW.phone, 1, 1) != '0')
BEGIN
    SELECT RAISE(FAIL, 'Invalid phone: must be 10 digits starting with 0');
END;

CREATE TRIGGER trg_reviews_rating_bi
BEFORE INSERT ON reviews
FOR EACH ROW
WHEN NEW.rating IS NULL OR NEW.rating < 1 OR NEW.rating > 5
BEGIN
    SELECT RAISE(FAIL, 'Invalid review rating: must be 1..5');
END;

CREATE TRIGGER trg_reviews_rating_bu
BEFORE UPDATE ON reviews
FOR EACH ROW
WHEN NEW.rating IS NULL OR NEW.rating < 1 OR NEW.rating > 5
BEGIN
    SELECT RAISE(FAIL, 'Invalid review rating: must be 1..5');
END;