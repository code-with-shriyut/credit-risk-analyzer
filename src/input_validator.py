def validate_input(name, age, income, loan_amount, tenure_months):
    if name == "" or name.strip() == "":
        raise ValueError("Name field cannot be empty!")
    if age < 18 or age > 70:
        raise ValueError("Age should be more than 18 and less than 70!")
    if income <= 0:
        raise ValueError("Monthly income must be greater than 0!")
    if loan_amount <= 0:
        raise ValueError("Fill valid loan amount!")
    if tenure_months < 1 or tenure_months > 360:
        raise ValueError("Provide with valid tenure period!")
    
    return True
