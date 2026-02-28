def evaluate_decision(risk):
    if risk == "LOW RISK":
        return "Loan Request Approved"
    elif risk == "MEDIUM RISK":
        return "Reviewing Your Request"
    else:
        return "Loan Request Rejected!"
