-- ============================================
-- Student Study Planner - Database Setup
-- Run this file in MySQL before starting app
-- ============================================

CREATE DATABASE IF NOT EXISTS study_planner;
USE study_planner;

-- Drop tables if re-running setup
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS users;

-- USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    prn VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SUBJECTS TABLE
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- TASKS TABLE
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    deadline DATE NOT NULL,
    status ENUM('Pending','Completed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- ============================================
-- SAMPLE DATA (optional - for testing)
-- Note: Register a real user through the app
-- to get a proper hashed password.
-- ============================================

-- Example: After registering user through app, you can insert sample subjects/tasks:
-- INSERT INTO subjects (user_id, subject_name) VALUES (1,'Data Structures'),(1,'DBMS'),(1,'OS');
-- INSERT INTO tasks (user_id, subject_id, task_name, deadline, status) VALUES
-- (1,1,'Binary Tree Assignment','2025-06-10','Pending'),
-- (1,2,'SQL Joins Practice','2025-06-05','Completed');
