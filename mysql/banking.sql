CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(10),
    password VARCHAR(255), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE Accounts (
    user_id int,
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    account_type ENUM('Savings', 'Checking', 'Loan'),
    balance DECIMAL(15,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

