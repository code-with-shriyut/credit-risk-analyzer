def risk_classification(
    ext_source_avg: float,
    days_employed: int,
    amt_annuity: float,
    amt_income_total: float,
    days_birth: int
) -> str:
    """
    Rule-based risk classification using Home Credit features.
    Acts as a secondary check alongside ML model prediction.
    Returns: LOW RISK / MEDIUM RISK / HIGH RISK
    """
    risk_points = 0

    # EMI ratio — annuity to income
    emi_ratio = amt_annuity / amt_income_total if amt_income_total > 0 else 1.0
    if emi_ratio <= 0.25:
        risk_points += 0
    elif emi_ratio <= 0.45:
        risk_points += 1
    else:
        risk_points += 2

    # External score average (replaces credit score)
    # EXT_SOURCE values are 0-1, higher is better
    if ext_source_avg < 0.3:
        risk_points += 2
    elif ext_source_avg < 0.5:
        risk_points += 1

    # Employment (DAYS_EMPLOYED is negative if employed)
    employed_months = abs(days_employed) / 30 if days_employed < 0 else 0
    if employed_months < 6:
        risk_points += 2
    elif employed_months < 12:
        risk_points += 1

    # Age (DAYS_BIRTH is negative)
    age_years = abs(days_birth) / 365
    if age_years < 23 or age_years > 60:
        risk_points += 1

    if risk_points <= 1:
        return "LOW RISK"
    elif risk_points == 2:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"