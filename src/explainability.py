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