from db import insert_loan_application
from input_validator import validate_input
from emi import calculate_emi
from risk import risk_classification
from decision import evaluate_decision

name = input("Name: ")
age = int(input("Age: "))
income = float(input("Monthly Income: "))
loan_amount = float(input("Loan Amount: "))
tenure_months = int(input("Tenure (months): "))
annual_rate = float(input("Annual Interest Rate: "))
credit_score = int(input("Credit Score: "))
months_employed = int(input("Months Employed: "))

validate_input(name, age, income, loan_amount, tenure_months)

emi = calculate_emi(loan_amount, annual_rate, tenure_months)
print("Monthly EMI:", emi)

emi_ratio = emi / income


risk = risk_classification(emi_ratio, age, tenure_months, credit_score, months_employed)
print(risk)

decision = evaluate_decision(risk)
print(decision)

insert_loan_application(
    name,
    age,
    income,
    loan_amount,
    tenure_months,
    annual_rate,
    credit_score,
    months_employed,
    emi,
    emi_ratio,
    risk,
    decision
)
