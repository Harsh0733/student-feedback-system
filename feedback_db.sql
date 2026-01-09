CREATE DATABASE IF NOT EXISTS feedback_db;
USE feedback_db;

CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    subject VARCHAR(100),
    message TEXT
);