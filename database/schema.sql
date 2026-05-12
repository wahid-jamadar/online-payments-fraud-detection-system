CREATE DATABASE IF NOT EXISTS fraud_db;
USE fraud_db;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    step INT,
    type VARCHAR(50),
    amount DECIMAL(12,2),
    oldbalanceOrg DECIMAL(12,2),
    newbalanceOrig DECIMAL(12,2),
    oldbalanceDest DECIMAL(12,2),
    newbalanceDest DECIMAL(12,2),
    prediction VARCHAR(20),
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password)
VALUES ('admin', 'admin123');

DELETE FROM users;

INSERT INTO users(username,password)
VALUES('admin', 'PASTE_HASH_HERE');