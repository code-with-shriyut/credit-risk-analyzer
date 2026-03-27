from src.db import get_db, save_loan_application
from sqlalchemy import text


def test_db_insert():
    db = next(get_db())

    test_id = "test_case_123"

    data = {
        "application_id": test_id,
        "full_name": "Test User",
        "decision": "APPROVED",
        "risk_category": "LOW RISK",
        "default_probability": 0.1,
        "processed_by": "admin"
    }

    # Insert data
    save_loan_application(db, data)

    # Fetch inserted record
    result = db.execute(
        text("SELECT * FROM loan_applications WHERE application_id = :id"),
        {"id": test_id}
    ).fetchone()

    assert result is not None

    # Optional cleanup (recommended)
    db.execute(
        text("DELETE FROM loan_applications WHERE application_id = :id"),
        {"id": test_id}
    )
    db.commit()