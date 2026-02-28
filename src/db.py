import sqlite3

DB_PATH = "data/loan_applications.db"


def insert_loan_application(
    name,
    age,
    monthly_income,
    loan_amount,
    tenure_months,
    annual_interest_rate,
    credit_score,
    months_employed,
    emi,
    emi_ratio,
    risk_category,
    decision
):
    """
    Insert a single loan application into the database.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO loan_applications (
            name,
            age,
            monthly_income,
            loan_amount,
            tenure_months,
            annual_interest_rate,
            credit_score,
            months_employed,
            emi,
            emi_ratio,
            risk_category,
            decision
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            age,
            monthly_income,
            loan_amount,
            tenure_months,
            annual_interest_rate,
            credit_score,
            months_employed,
            emi,
            emi_ratio,
            risk_category,
            decision
        )
    )

    conn.commit()
    conn.close()