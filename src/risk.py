def risk_classification(emi_ratio, age, tenure_months, credit_score, months_employed):
    
    # ##########
    # Rule-based risk classification using:
    # - EMI emi_ratio
    # - Age risk
    # - Tenure risk

    # Returns: LOW RISK / MEDIUM RISK / HIGH RISK
    # ###########

    risk_points = 0

    if emi_ratio <= 0.25:
        risk_points += 0
    elif emi_ratio <= 0.45:
        risk_points +=1
    else:
        risk_points += 2

    if credit_score < 550:
        risk_points += 2
    elif credit_score < 650:
        risk_points += 1

    if months_employed < 6:
        risk_points += 2
    elif months_employed < 12:
        risk_points += 1

    if age < 23 or age > 60:
        risk_points += 1

    if tenure_months > 60:
        risk_points += 1

    if risk_points <= 1:
        return "LOW RISK"
    elif risk_points == 2:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"
    