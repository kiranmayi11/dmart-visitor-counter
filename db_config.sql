CREATE DATABASE dmart;

USE dmart;

CREATE TABLE visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    comment TEXT,
    date DATE DEFAULT (CURRENT_DATE)
);
