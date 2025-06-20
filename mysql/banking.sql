USE bankdb;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(10),
    password VARCHAR(255), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Accounts (
    user_id INT,
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    balance DECIMAL(15,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    amount DECIMAL(15,2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

CREATE TABLE Admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(100)
);
