from src.ml_model import predict


def get_sample_input():
    """Reusable sample input for ML model"""
    return {
        "AMT_INCOME_TOTAL": 60000,
        "AMT_CREDIT": 300000,
        "AMT_ANNUITY": 15000,
        "AMT_GOODS_PRICE": 250000,
        "DAYS_BIRTH": -12000,
        "DAYS_EMPLOYED": -1000,
        "EXT_SOURCE_1": 0.5,
        "EXT_SOURCE_2": 0.5,
        "EXT_SOURCE_3": 0.5,
        "CODE_GENDER": 1,
        "FLAG_OWN_CAR": 1,
        "FLAG_OWN_REALTY": 1
    }


# -------------------------------
# Basic Output Structure Test
# -------------------------------
def test_model_returns_required_keys():
    result = predict(get_sample_input())

    assert "default_probability" in result
    assert "prediction" in result
    assert "risk_label" in result
    assert "shap_explanation" in result


# -------------------------------
# Probability Range Test
# -------------------------------
def test_probability_is_valid():
    result = predict(get_sample_input())

    prob = result["default_probability"]
    assert 0 <= prob <= 1


# -------------------------------
# Prediction Type Test
# -------------------------------
def test_prediction_is_binary():
    result = predict(get_sample_input())

    assert result["prediction"] in [0, 1]


# -------------------------------
# Risk Label Consistency Test
# -------------------------------
def test_risk_label_matches_prediction():
    result = predict(get_sample_input())

    if result["prediction"] == 1:
        assert result["risk_label"] == "HIGH RISK"
    else:
        assert result["risk_label"] == "LOW RISK"


# -------------------------------
# SHAP Explanation Test
# -------------------------------
def test_shap_explanation_structure():
    result = predict(get_sample_input())

    shap_data = result["shap_explanation"]

    assert isinstance(shap_data, list)
    assert len(shap_data) > 0

    for item in shap_data:
        assert "feature" in item
        assert "impact" in item
        assert "message" in item


# -------------------------------
# Missing Optional Fields Test
# -------------------------------
def test_missing_optional_fields():
    input_data = {
        "AMT_INCOME_TOTAL": 50000,
        "AMT_CREDIT": 200000,
        "AMT_ANNUITY": 10000,
        "DAYS_BIRTH": -12000,
        "DAYS_EMPLOYED": -1000
    }

    result = predict(input_data)

    assert "default_probability" in result


# -------------------------------
# Extreme Case Test
# -------------------------------
def test_extreme_high_risk_case():
    input_data = {
        "AMT_INCOME_TOTAL": 20000,
        "AMT_CREDIT": 800000,
        "AMT_ANNUITY": 40000,
        "AMT_GOODS_PRICE": 700000,
        "DAYS_BIRTH": -8000,
        "DAYS_EMPLOYED": 100,  # unemployed
        "EXT_SOURCE_1": 0.1,
        "EXT_SOURCE_2": 0.1,
        "EXT_SOURCE_3": 0.1,
        "CODE_GENDER": 1,
        "FLAG_OWN_CAR": 0,
        "FLAG_OWN_REALTY": 0
    }

    result = predict(input_data)

    assert result["prediction"] in [0, 1]
    assert result["risk_label"] in ["LOW RISK", "HIGH RISK"]