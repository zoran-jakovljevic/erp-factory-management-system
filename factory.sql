-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 08, 2024 at 07:52 PM
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
-- Database: `factory`
--

-- --------------------------------------------------------

--
-- Table structure for table `materials`
--

CREATE TABLE `materials` (
  `material_id` int(11) NOT NULL,
  `material_name` varchar(100) NOT NULL,
  `purchase_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `materials`
--

INSERT INTO `materials` (`material_id`, `material_name`, `purchase_price`) VALUES
(1, 'Aluminum', 15.50),
(2, 'Plastic', 5.20),
(3, 'Steel', 22.75),
(4, 'Glass', 8.30),
(5, 'Copper', 10.00),
(6, 'Rubber', 3.75),
(7, 'Wood', 7.50),
(8, 'Fabric', 4.60),
(9, 'Leather', 9.80),
(10, 'Silicon', 12.40);

-- --------------------------------------------------------

--
-- Table structure for table `material_inventory`
--

CREATE TABLE `material_inventory` (
  `inventory_id` int(11) NOT NULL,
  `material_id` int(11) DEFAULT NULL,
  `material_quantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `material_inventory`
--

INSERT INTO `material_inventory` (`inventory_id`, `material_id`, `material_quantity`) VALUES
(1, 1, 5200.00),
(2, 2, 498.50),
(3, 3, 145.00),
(4, 4, 550.00),
(5, 5, 99.80),
(6, 6, 250.00),
(7, 7, 120.00),
(8, 8, 400.00),
(9, 9, 50.00),
(10, 10, 79.90);

-- --------------------------------------------------------

--
-- Table structure for table `material_products`
--

CREATE TABLE `material_products` (
  `product_id` int(11) NOT NULL,
  `material_id` int(11) NOT NULL,
  `required_quantity` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `material_products`
--

INSERT INTO `material_products` (`product_id`, `material_id`, `required_quantity`) VALUES
(1, 2, 1.50),
(1, 3, 5.00),
(2, 5, 0.20),
(2, 10, 0.10),
(3, 5, 1.00),
(3, 10, 0.50),
(4, 7, 10.00),
(5, 7, 5.00),
(6, 2, 0.25),
(7, 1, 0.50);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `selling_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `selling_price`) VALUES
(1, 'Bicycle', 150.00),
(2, 'Smartphone', 300.00),
(3, 'Laptop', 850.00),
(4, 'Desk', 120.00),
(5, 'Chair', 60.00),
(6, 'Headphones', 50.00),
(7, 'Water Bottle', 15.00),
(8, 'Sunglasses', 25.00),
(9, 'Jacket', 80.00),
(10, 'Backpack', 45.00);

-- --------------------------------------------------------

--
-- Table structure for table `product_inventory`
--

CREATE TABLE `product_inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_inventory`
--

INSERT INTO `product_inventory` (`inventory_id`, `product_id`, `product_quantity`) VALUES
(1, 1, 21),
(2, 2, 16),
(3, 3, 9),
(4, 4, 30),
(5, 5, 25),
(6, 6, 50),
(7, 7, 100),
(8, 8, 40),
(9, 9, 15),
(10, 10, 35);

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `transaction_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_quantity` int(11) NOT NULL,
  `transaction_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`transaction_id`, `product_id`, `product_quantity`, `transaction_date`) VALUES
(1, 1, 2, '2024-10-05'),
(2, 2, 1, '2024-10-06'),
(3, 3, 3, '2024-10-07'),
(4, 4, 5, '2024-10-08'),
(5, 5, 7, '2024-10-09'),
(6, 6, 10, '2024-10-10'),
(7, 7, 20, '2024-10-11'),
(8, 8, 8, '2024-10-12'),
(9, 9, 4, '2024-10-13'),
(10, 10, 6, '2024-10-14'),
(11, 1, 5, '2024-11-08'),
(12, 3, 1, '2024-11-08');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `materials`
--
ALTER TABLE `materials`
  ADD PRIMARY KEY (`material_id`);

--
-- Indexes for table `material_inventory`
--
ALTER TABLE `material_inventory`
  ADD PRIMARY KEY (`inventory_id`),
  ADD KEY `material_id` (`material_id`);

--
-- Indexes for table `material_products`
--
ALTER TABLE `material_products`
  ADD PRIMARY KEY (`product_id`,`material_id`),
  ADD KEY `material_id` (`material_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `product_inventory`
--
ALTER TABLE `product_inventory`
  ADD PRIMARY KEY (`inventory_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `materials`
--
ALTER TABLE `materials`
  MODIFY `material_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `material_inventory`
--
ALTER TABLE `material_inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `product_inventory`
--
ALTER TABLE `product_inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `material_inventory`
--
ALTER TABLE `material_inventory`
  ADD CONSTRAINT `material_inventory_ibfk_1` FOREIGN KEY (`material_id`) REFERENCES `materials` (`material_id`) ON DELETE CASCADE;

--
-- Constraints for table `material_products`
--
ALTER TABLE `material_products`
  ADD CONSTRAINT `material_products_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `material_products_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`material_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_inventory`
--
ALTER TABLE `product_inventory`
  ADD CONSTRAINT `product_inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
