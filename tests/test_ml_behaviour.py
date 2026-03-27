from src.ml_model import predict


def test_extreme_values_behavior():
    """Extreme bad inputs should have higher risk than normal inputs"""

    normal = predict({
        "AMT_INCOME_TOTAL": 80000,
        "AMT_CREDIT": 200000,
        "AMT_ANNUITY": 10000,
        "DAYS_BIRTH": -12000,
        "DAYS_EMPLOYED": -2000,
        "EXT_SOURCE_1": 0.7,
        "EXT_SOURCE_2": 0.7,
        "EXT_SOURCE_3": 0.7,
        "CODE_GENDER": 1,
        "FLAG_OWN_CAR": 1,
        "FLAG_OWN_REALTY": 1
    })

    extreme = predict({
        "AMT_INCOME_TOTAL": 10000,
        "AMT_CREDIT": 900000,
        "AMT_ANNUITY": 50000,
        "DAYS_BIRTH": -7000,
        "DAYS_EMPLOYED": 50,
        "EXT_SOURCE_1": 0.1,
        "EXT_SOURCE_2": 0.1,
        "EXT_SOURCE_3": 0.1,
        "CODE_GENDER": 1,
        "FLAG_OWN_CAR": 0,
        "FLAG_OWN_REALTY": 0
    })

    assert extreme["default_probability"] >= normal["default_probability"]