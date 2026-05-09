def get_reason_codes(shap_dict):
    sorted_features = sorted(
        shap_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    reason_codes = []

    for feature, value in sorted_features[:3]:
        direction = "POSITIVE" if value < 0 else "NEGATIVE"
        reason_codes.append(f"{feature.upper()}_{direction}")

    return reason_codes

def get_reason_codes(shap_dict):
    sorted_features = sorted(
        shap_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    reason_codes = []

    for feature, value in sorted_features[:3]:
        direction = "POSITIVE" if value < 0 else "NEGATIVE"
        reason_codes.append(f"{feature.upper()}_{direction}")

    return reason_codes


def reason_to_text(code: str):

    mapping = {
        "HIGH_FOIR": "financial obligations are high relative to income",

        "LOW_INCOME": "monthly income is below the recommended affordability threshold",

        "EXT_SOURCE_1_POSITIVE": "banking behavior appears financially stable",
        "EXT_SOURCE_2_POSITIVE": "UPI transaction activity appears healthy",
        "EXT_SOURCE_3_POSITIVE": "utility payment behavior appears reliable",

        "EXT_SOURCE_1_NEGATIVE": "banking behavior indicates elevated financial risk",
        "EXT_SOURCE_2_NEGATIVE": "UPI transaction behavior shows repayment risk",
        "EXT_SOURCE_3_NEGATIVE": "utility payment behavior appears unstable",

        "AMT_CREDIT_NEGATIVE": "loan amount is relatively high",
        "AMT_ANNUITY_NEGATIVE": "EMI burden is high",
        "AMT_INCOME_TOTAL_NEGATIVE": "income level appears insufficient"
    }

    return mapping.get(code, code.replace("_", " ").lower())

def generate_explanation(reason_codes: list) -> str:
    """
    Convert reason codes into human-readable explanation
    """

    explanations = []

    for code in reason_codes:
        explanations.append(reason_to_text(code))

    if not explanations:
        return "No major risk indicators detected."

    return (
        "The applicant shows elevated repayment risk because "
        + ", ".join(explanations)
        + "."
    )