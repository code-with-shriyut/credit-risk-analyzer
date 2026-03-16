import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Main database engine — connects to Supabase PostgreSQL
engine = create_engine(DATABASE_URL)

# Session factory — creates a new session for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session per request, closes after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: Session, username: str):
    """Fetch user from DB by username — used during login."""
    result = db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": username}
    ).fetchone()
    return result


def save_loan_application(db: Session, data: dict):
    """Insert a loan application record into the database after prediction."""
    db.execute(
        text("""
            INSERT INTO loan_applications 
            (application_id, full_name, decision, risk_category, default_probability, processed_by)
            VALUES 
            (:application_id, :full_name, :decision, :risk_category, :default_probability, :processed_by)
        """),
        data
    )
    db.commit()