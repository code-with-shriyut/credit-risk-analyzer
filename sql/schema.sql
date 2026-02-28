CREATE TABLE loan_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    monthly_income REAL NOT NULL,

    loan_amount REAL NOT NULL,
    tenure_months INTEGER NOT NULL,
    annual_interest_rate REAL NOT NULL,

    credit_score INTEGER,
    months_employed INTEGER,

    emi REAL NOT NULL,
    emi_ratio REAL NOT NULL,

    risk_category TEXT NOT NULL,
    decision TEXT NOT NULL
);

