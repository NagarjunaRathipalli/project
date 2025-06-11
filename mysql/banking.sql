CREATE TABLE withdrawals (
    withdrawal_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    withdrawal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method VARCHAR(50), 
    status VARCHAR(20) DEFAULT 
    reference_note TEXT,

    CONSTRAINT fk_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE
);