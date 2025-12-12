-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 12, 2025 at 12:02 AM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gurmesea_airline_strike`
--

-- --------------------------------------------------------

--
-- Table structure for table `gurmesea_aircraft`
--

CREATE TABLE `gurmesea_aircraft` (
  `plane_id` int NOT NULL,
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `mass` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `manufacturer` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `model_family` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `variant` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `aircraft` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gurmesea_airlines`
--

CREATE TABLE `gurmesea_airlines` (
  `aid` int NOT NULL,
  `airline` varchar(100) NOT NULL,
  `callsign` varchar(50) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `icao` char(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gurmesea_airports`
--

CREATE TABLE `gurmesea_airports` (
  `aid` int NOT NULL,
  `name` varchar(150) NOT NULL,
  `city_code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `icao` char(4) NOT NULL,
  `latitude_deg` decimal(9,6) DEFAULT NULL,
  `longitude_deg` decimal(9,6) DEFAULT NULL,
  `country` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gurmesea_incidents`
--

CREATE TABLE `gurmesea_incidents` (
  `record_id` int NOT NULL,
  `incident_date` date DEFAULT NULL,
  `operator_id` int DEFAULT NULL,
  `aircraft_id` int DEFAULT NULL,
  `airport_id` int DEFAULT NULL,
  `flight_phase` varchar(50) DEFAULT NULL,
  `visibility` varchar(50) DEFAULT NULL,
  `precipitation` varchar(50) DEFAULT NULL,
  `height` float DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `distance` float DEFAULT NULL,
  `species_id` int DEFAULT NULL,
  `species_quantity` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gurmesea_species`
--

CREATE TABLE `gurmesea_species` (
  `sid` int NOT NULL,
  `species_name` varchar(200) NOT NULL,
  `class` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gurmesea_aircraft`
--
ALTER TABLE `gurmesea_aircraft`
  ADD PRIMARY KEY (`plane_id`);

--
-- Indexes for table `gurmesea_airlines`
--
ALTER TABLE `gurmesea_airlines`
  ADD PRIMARY KEY (`aid`);

--
-- Indexes for table `gurmesea_airports`
--
ALTER TABLE `gurmesea_airports`
  ADD PRIMARY KEY (`aid`),
  ADD UNIQUE KEY `uk_airports_icao` (`icao`);

--
-- Indexes for table `gurmesea_incidents`
--
ALTER TABLE `gurmesea_incidents`
  ADD PRIMARY KEY (`record_id`),
  ADD KEY `operator_id` (`operator_id`),
  ADD KEY `species_id` (`species_id`),
  ADD KEY `aircraft_id` (`aircraft_id`),
  ADD KEY `airport_id` (`airport_id`);

--
-- Indexes for table `gurmesea_species`
--
ALTER TABLE `gurmesea_species`
  ADD PRIMARY KEY (`sid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gurmesea_aircraft`
--
ALTER TABLE `gurmesea_aircraft`
  MODIFY `plane_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gurmesea_airlines`
--
ALTER TABLE `gurmesea_airlines`
  MODIFY `aid` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gurmesea_airports`
--
ALTER TABLE `gurmesea_airports`
  MODIFY `aid` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gurmesea_species`
--
ALTER TABLE `gurmesea_species`
  MODIFY `sid` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
