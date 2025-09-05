-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 05, 2025 at 12:05 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travel_tour_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `customername` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `customername`, `password_hash`, `email`) VALUES
(1, 'admin', '123', 'trungkien09122004@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `travel_date` date NOT NULL,
  `num_travelers` int(11) DEFAULT 1,
  `status` enum('pending','confirmed','canceled') DEFAULT 'pending',
  `total_amount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `customer_id`, `service_id`, `booking_date`, `travel_date`, `num_travelers`, `status`, `total_amount`) VALUES
(1, 1, 1, '2025-09-05 10:02:20', '2025-09-10', 2, 'confirmed', 300.00),
(2, 2, 2, '2025-09-05 10:02:20', '2025-09-12', 1, 'pending', 200.00),
(3, 3, 3, '2025-09-05 10:02:20', '2025-09-15', 3, 'confirmed', 540.00),
(4, 4, 4, '2025-09-05 10:02:20', '2025-09-18', 1, 'canceled', 220.00),
(5, 5, 5, '2025-09-05 10:02:20', '2025-09-10', 2, 'confirmed', 180.00),
(6, 6, 6, '2025-09-05 10:02:20', '2025-09-12', 1, 'pending', 120.00),
(7, 7, 9, '2025-09-05 10:02:20', '2025-09-11', 2, 'confirmed', 600.00),
(8, 8, 10, '2025-09-05 10:02:20', '2025-09-13', 2, 'confirmed', 500.00),
(9, 9, 11, '2025-09-05 10:02:20', '2025-09-16', 1, 'pending', 200.00),
(10, 10, 12, '2025-09-05 10:02:20', '2025-09-19', 3, 'confirmed', 840.00);

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `full_name`, `email`, `password_hash`, `phone`, `address`) VALUES
(1, 'hạnh', 'hanh@example.com', '123', '0912345678', 'Hà Nội'),
(2, 'hoàng', 'hoang@example.com', '234', '0923456789', 'Đà Nẵng'),
(3, 'hùng', 'hung@example.com', '345', '0934567890', 'Hải Phòng'),
(4, 'long', 'long@example.com', '456', '0945678901', 'Hồ Chí Minh'),
(5, 'kien', 'kien@example.com', '567', '0956789012', 'Cần Thơ'),
(6, 'Do Thi F', 'f@example.com', '678', '0967890123', 'Huế'),
(7, 'Vu Van G', 'g@example.com', '789', '0978901234', 'Quảng Ninh'),
(8, 'Bui Thi H', 'h@example.com', '890', '0989012345', 'Nha Trang'),
(9, 'Ngo Van I', 'i@example.com', '901', '0990123456', 'Đà Lạt'),
(10, 'Dang Thi J', 'j@example.com', '012', '0901234567', 'Phú Quốc');

--
-- Triggers `customers`
--
DELIMITER $$
CREATE TRIGGER `trg_customers_phone_bi` BEFORE INSERT ON `customers` FOR EACH ROW BEGIN
  IF NEW.phone IS NOT NULL AND NEW.phone NOT REGEXP '^[0][0-9]{9}$' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid phone: must be 10 digits starting with 0';
  END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_customers_phone_bu` BEFORE UPDATE ON `customers` FOR EACH ROW BEGIN
  IF NEW.phone IS NOT NULL AND NEW.phone NOT REGEXP '^[0][0-9]{9}$' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid phone: must be 10 digits starting with 0';
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `payment_method` enum('credit_card','e_wallet','gateway') DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` enum('pending','paid','failed') DEFAULT 'pending',
  `transaction_ref` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `booking_id`, `payment_date`, `payment_method`, `amount`, `status`, `transaction_ref`) VALUES
(1, 1, '2025-09-05 10:02:38', 'credit_card', 300.00, 'paid', 'TXN1001'),
(2, 2, '2025-09-05 10:02:38', 'e_wallet', 200.00, 'pending', 'TXN1002'),
(3, 3, '2025-09-05 10:02:38', 'credit_card', 540.00, 'paid', 'TXN1003'),
(4, 4, '2025-09-05 10:02:38', 'gateway', 220.00, 'failed', 'TXN1004'),
(5, 5, '2025-09-05 10:02:38', 'credit_card', 180.00, 'paid', 'TXN1005'),
(6, 6, '2025-09-05 10:02:38', 'e_wallet', 120.00, 'pending', 'TXN1006'),
(7, 7, '2025-09-05 10:02:38', 'gateway', 600.00, 'paid', 'TXN1007'),
(8, 8, '2025-09-05 10:02:38', 'credit_card', 500.00, 'paid', 'TXN1008'),
(9, 9, '2025-09-05 10:02:38', 'e_wallet', 200.00, 'pending', 'TXN1009'),
(10, 10, '2025-09-05 10:02:38', 'gateway', 840.00, 'paid', 'TXN1010');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`review_id`, `customer_id`, `service_id`, `rating`, `comment`, `created_at`) VALUES
(1, 1, 1, 5, 'Dịch vụ bay tuyệt vời', '2025-09-05 10:02:48'),
(2, 2, 2, 4, 'Chuyến bay an toàn và nhanh chóng', '2025-09-05 10:02:48'),
(3, 3, 3, 5, 'Giá rẻ, phục vụ tốt', '2025-09-05 10:02:48'),
(4, 4, 4, 3, 'Chuyến bay hơi trễ giờ', '2025-09-05 10:02:48'),
(5, 5, 5, 4, 'Khách sạn sang trọng, vị trí đẹp', '2025-09-05 10:02:48'),
(6, 6, 6, 5, 'Resort tuyệt vời, nhân viên thân thiện', '2025-09-05 10:02:48'),
(7, 7, 9, 5, 'Tour Hạ Long quá đẹp', '2025-09-05 10:02:48'),
(8, 8, 10, 4, 'Tour Sapa hợp lý, hướng dẫn viên nhiệt tình', '2025-09-05 10:02:48'),
(9, 9, 11, 5, 'Phú Quốc biển xanh cát trắng', '2025-09-05 10:02:48'),
(10, 10, 12, 4, 'Tour Bà Nà Hills thú vị', '2025-09-05 10:02:48');

--
-- Triggers `reviews`
--
DELIMITER $$
CREATE TRIGGER `trg_reviews_rating_bi` BEFORE INSERT ON `reviews` FOR EACH ROW BEGIN
  IF NEW.rating IS NULL OR NEW.rating < 1 OR NEW.rating > 5 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid review rating: must be 1..5';
  END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_reviews_rating_bu` BEFORE UPDATE ON `reviews` FOR EACH ROW BEGIN
  IF NEW.rating IS NULL OR NEW.rating < 1 OR NEW.rating > 5 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid review rating: must be 1..5';
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `traveler_details`
--

CREATE TABLE `traveler_details` (
  `traveler_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `gender` enum('male','female','other') DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `traveler_details`
--

INSERT INTO `traveler_details` (`traveler_id`, `booking_id`, `full_name`, `gender`, `dob`, `passport_number`) VALUES
(1, 1, 'hạnh', 'female', '1990-01-01', 'VN123456'),
(2, 2, 'hoàng', 'male', '1992-02-02', 'VN223344'),
(3, 3, 'hùng', 'male', '1989-03-03', 'VN334455'),
(4, 4, 'long', 'male', '1995-04-04', 'VN445566'),
(5, 5, 'kien', 'male', '1988-05-05', 'VN556677'),
(6, 6, 'Do Thi F', 'female', '1993-06-06', 'VN667788'),
(7, 7, 'Vu Van G', 'male', '1991-07-07', 'VN778899'),
(8, 8, 'Bui Thi H', 'female', '1994-08-08', 'VN889900'),
(9, 9, 'Ngo Van I', 'male', '1990-09-09', 'VN990011'),
(10, 10, 'Dang Thi J', 'female', '1996-10-10', 'VN110022');

-- --------------------------------------------------------

--
-- Table structure for table `travel_services`
--

CREATE TABLE `travel_services` (
  `service_id` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `service_type` enum('flight','hotel','tour') NOT NULL,
  `title` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `travel_services`
--

INSERT INTO `travel_services` (`service_id`, `price`, `rating`, `destination`, `service_type`, `title`, `description`, `start_date`, `end_date`, `created_at`) VALUES
(1, 150.00, 4.5, 'Hà Nội', 'flight', 'Vietnam Airlines Hà Nội - HCM', 'Chuyến bay khứ hồi Hà Nội - TP.HCM', '2025-09-01', '2025-09-30', '2025-09-05 10:02:11'),
(2, 200.00, 4.7, 'Đà Nẵng', 'flight', 'Bamboo Airways Đà Nẵng - Hà Nội', 'Chuyến bay tiết kiệm Đà Nẵng - Hà Nội', '2025-09-05', '2025-09-30', '2025-09-05 10:02:11'),
(3, 180.00, 4.3, 'Hồ Chí Minh', 'flight', 'Vietjet Air HCM - Đà Lạt', 'Chuyến bay giá rẻ HCM - Đà Lạt', '2025-09-03', '2025-09-30', '2025-09-05 10:02:11'),
(4, 220.00, 4.6, 'Phú Quốc', 'flight', 'Vietnam Airlines HCM - Phú Quốc', 'Chuyến bay HCM - Phú Quốc cao cấp', '2025-09-02', '2025-09-30', '2025-09-05 10:02:11'),
(5, 90.00, 4.8, 'Hà Nội', 'hotel', 'Khách sạn Metropole Hà Nội', 'Khách sạn 5 sao trung tâm Hà Nội', '2025-09-01', '2025-09-30', '2025-09-05 10:02:11'),
(6, 120.00, 4.5, 'Đà Nẵng', 'hotel', 'Resort Furama Đà Nẵng', 'Resort biển sang trọng tại Đà Nẵng', '2025-09-01', '2025-09-30', '2025-09-05 10:02:11'),
(7, 80.00, 4.2, 'Nha Trang', 'hotel', 'Khách sạn Vinpearl Nha Trang', 'Khách sạn cao cấp với view biển đẹp', '2025-09-01', '2025-09-30', '2025-09-05 10:02:11'),
(8, 110.00, 4.4, 'Đà Lạt', 'hotel', 'Terracotta Đà Lạt', 'Resort sang trọng giữa rừng thông Đà Lạt', '2025-09-01', '2025-09-30', '2025-09-05 10:02:11'),
(9, 300.00, 4.9, 'Hạ Long', 'tour', 'Tour Du Thuyền Vịnh Hạ Long 3N2Đ', 'Khám phá Vịnh Hạ Long bằng du thuyền', '2025-09-10', '2025-09-12', '2025-09-05 10:02:11'),
(10, 250.00, 4.7, 'Sapa', 'tour', 'Tour Sapa Fansipan 2N1Đ', 'Khám phá núi Fansipan và bản làng Sapa', '2025-09-15', '2025-09-16', '2025-09-05 10:02:11'),
(11, 400.00, 4.8, 'Phú Quốc', 'tour', 'Tour Phú Quốc 3N2Đ', 'Trải nghiệm biển đảo Phú Quốc tuyệt đẹp', '2025-09-20', '2025-09-22', '2025-09-05 10:02:11'),
(12, 280.00, 4.6, 'Đà Nẵng', 'tour', 'Tour Bà Nà Hills 1N', 'Tham quan Bà Nà Hills và Cầu Vàng', '2025-09-18', '2025-09-18', '2025-09-05 10:02:11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `customername` (`customername`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `fk_bookings_customer` (`customer_id`),
  ADD KEY `fk_bookings_service` (`service_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD UNIQUE KEY `transaction_ref` (`transaction_ref`),
  ADD KEY `fk_payments_booking` (`booking_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `fk_reviews_customer` (`customer_id`),
  ADD KEY `fk_reviews_service` (`service_id`);

--
-- Indexes for table `traveler_details`
--
ALTER TABLE `traveler_details`
  ADD PRIMARY KEY (`traveler_id`),
  ADD KEY `fk_travelers_booking` (`booking_id`);

--
-- Indexes for table `travel_services`
--
ALTER TABLE `travel_services`
  ADD PRIMARY KEY (`service_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `traveler_details`
--
ALTER TABLE `traveler_details`
  MODIFY `traveler_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `travel_services`
--
ALTER TABLE `travel_services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `fk_bookings_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_bookings_service` FOREIGN KEY (`service_id`) REFERENCES `travel_services` (`service_id`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `fk_payments_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `fk_reviews_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_reviews_service` FOREIGN KEY (`service_id`) REFERENCES `travel_services` (`service_id`) ON DELETE CASCADE;

--
-- Constraints for table `traveler_details`
--
ALTER TABLE `traveler_details`
  ADD CONSTRAINT `fk_travelers_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
