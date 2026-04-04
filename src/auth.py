from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "credit_risk_analyzer_secret_key_2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ── Password hashing setup ────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── OAuth2 scheme ─────────────────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# ── Password utilities ────────────────────────────────────────────────────────
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
    
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ── JWT Token creation ────────────────────────────────────────────────────────
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ── JWT Token decoding ────────────────────────────────────────────────────────
def decode_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ── Role-based access control ─────────────────────────────────────────────────
def require_admin(current_user: dict = Depends(decode_token)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user