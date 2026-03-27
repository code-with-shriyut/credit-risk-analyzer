from src.risk import risk_classification


def test_low_risk_case():
    result = risk_classification(
        ext_source_avg=0.8,
        days_employed=-2000,
        amt_annuity=10000,
        amt_income_total=100000,
        days_birth=-12000
    )
    assert result == "LOW RISK"


def test_high_risk_case():
    result = risk_classification(
        ext_source_avg=0.2,
        days_employed=100,  # unemployed
        amt_annuity=40000,
        amt_income_total=20000,
        days_birth=-8000
    )
    assert result == "HIGH RISK"


def test_medium_risk_case():
    result = risk_classification(
        ext_source_avg=0.45,
        days_employed=-300,
        amt_annuity=20000,
        amt_income_total=60000,
        days_birth=-10000
    )
    assert result in ["MEDIUM RISK", "HIGH RISK"]


def test_unemployed_is_risky():
    result = risk_classification(
        ext_source_avg=0.6,
        days_employed=100,  # unemployed
        amt_annuity=10000,
        amt_income_total=100000,
        days_birth=-12000
    )
    assert result in ["MEDIUM RISK", "HIGH RISK"]


def test_low_ext_source_is_risky():
    result = risk_classification(
        ext_source_avg=0.2,
        days_employed=-1000,
        amt_annuity=10000,
        amt_income_total=100000,
        days_birth=-12000
    )
    assert result in ["MEDIUM RISK", "HIGH RISK"]