-- setup.sql
-- Database initialization for CLI Event & Study Manager

-- Create database
CREATE DATABASE IF NOT EXISTS student_manager;
USE student_manager;

-- Table for storing users
CREATE TABLE IF NOT EXISTS new_users (
    SNO INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Example event table (each user gets their own events_userX table dynamically in Python)
-- This is a template for reference
CREATE TABLE IF NOT EXISTS events_user1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day DATE,
    tasks VARCHAR(255),
    event_status VARCHAR(20) DEFAULT 'pending'
);

-- Example topics table (each student gets <studentname>_topics dynamically in Python)
-- This is a template for reference
CREATE TABLE IF NOT EXISTS sampleuser_topics (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    topic_name VARCHAR(255) NOT NULL,
    count INT DEFAULT 0,
    last_revised DATE,
    next_revision DATE
);
