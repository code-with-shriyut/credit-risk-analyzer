import sys
sys.path.insert(0, '.')

from src.auth import hash_password, verify_password, create_access_token


def test_hash_and_verify_correct_password():
    hashed = hash_password("testpass123")
    assert verify_password("testpass123", hashed)


def test_wrong_password_fails():
    hashed = hash_password("testpass123")
    assert not verify_password("wrongpassword", hashed)


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "testuser", "role": "analyst"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_different_passwords_have_different_hashes():
    hash1 = hash_password("password1")
    hash2 = hash_password("password1")
    # bcrypt adds salt — same password, different hash every time
    assert hash1 != hash2

def test_token_contains_data():
    token = create_access_token({"sub": "testuser", "role": "admin"})
    assert isinstance(token, str)
    assert len(token) > 10 # Basic check that token is not empty and looks like a JWT