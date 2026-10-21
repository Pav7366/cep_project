CREATE DATABASE IF NOT EXISTS financial_manager;
USE financial_manager;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    category VARCHAR(80) NOT NULL,
    transaction_date DATE NOT NULL,
    note TEXT,
    currency VARCHAR(10) DEFAULT 'INR',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    limit_amount DECIMAL(12, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE savings_goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_amount DECIMAL(12, 2) NOT NULL,
    deadline DATE NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE groups_table (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    group_type VARCHAR(40) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE group_members (
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES groups_table(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE group_expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    payer_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    category VARCHAR(80) NOT NULL,
    expense_date DATE NOT NULL,
    note TEXT,
    currency VARCHAR(10) DEFAULT 'INR',
    FOREIGN KEY (group_id) REFERENCES groups_table(group_id) ON DELETE CASCADE,
    FOREIGN KEY (payer_id) REFERENCES users(user_id)
);

CREATE TABLE expense_splits (
    expense_id INT NOT NULL,
    user_id INT NOT NULL,
    owed_amount DECIMAL(12, 2) NOT NULL,
    PRIMARY KEY (expense_id, user_id),
    FOREIGN KEY (expense_id) REFERENCES group_expenses(expense_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE debts (
    debt_id INT AUTO_INCREMENT PRIMARY KEY,
    lender_id INT NOT NULL,
    borrower_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    due_date DATE,
    note TEXT,
    status ENUM('pending', 'paid') DEFAULT 'pending',
    FOREIGN KEY (lender_id) REFERENCES users(user_id),
    FOREIGN KEY (borrower_id) REFERENCES users(user_id)
);

CREATE TABLE subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    cycle ENUM('weekly', 'monthly', 'quarterly', 'yearly') NOT NULL,
    next_due_date DATE NOT NULL,
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
