def calculate_emi(loan_amount, annual_rate, tenure_months):
    monthly_rate = annual_rate / (12 * 100)

    if monthly_rate == 0:
        emi = loan_amount / tenure_months
    else:

        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2) #rounding off the emi to 2 decimals

    return emi