from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def get_token():
    response = client.post(
        "/login",
        data={   # ✅ FIX HERE
            "username": "admin",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login():
    response = client.post(
        "/login",
        data={   # ✅ FIX HERE
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_predict_endpoint():
    token = get_token()

    response = client.post(
        "/predict",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "API Test User",
            "gender": "M",
            "age_years": 30,
            "AMT_INCOME_TOTAL": 60000,
            "AMT_CREDIT": 300000,
            "AMT_ANNUITY": 15000,
            "DAYS_BIRTH": -12000,
            "DAYS_EMPLOYED": -1000,
            "EXT_SOURCE_1": 0.5,
            "EXT_SOURCE_2": 0.5,
            "EXT_SOURCE_3": 0.5,
            "CODE_GENDER": 1,
            "FLAG_OWN_CAR": 1,
            "FLAG_OWN_REALTY": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "decision" in data
    assert "risk_category" in data
    assert "default_probability" in data
    assert "shap_explanation" in data


def test_protected_route_without_token():
    response = client.post("/predict", json={})
    assert response.status_code == 401