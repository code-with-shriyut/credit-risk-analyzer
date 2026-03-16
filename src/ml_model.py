import joblib 
import numpy as np
import pandas as pd
import shap
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# ── Load models once at startup ────────────────────────────────────────────────
model = joblib.load(MODELS_DIR / "xgb_model.pkl")

scaler = joblib.load(MODELS_DIR / "scaler.pkl")

feature_columns = joblib.load(MODELS_DIR / "feature_columns.pkl")

# SHAP explainer — uses TreeExplainer for XGBoost (fast, no background data needed)
explainer = shap.TreeExplainer(model)


def predict(input_dict: dict) -> dict:
    """
    Takes raw input dict, preprocesses it, runs XGBoost prediction,
    and returns probability + SHAP explanation for top 5 features.
    """
    # Step 1: Convert to DataFrame and align with training feature columns
    df = pd.DataFrame([input_dict])
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Step 2: Scale
    scaled = scaler.transform(df)

    # Step 3: Predict
    prob = float(model.predict_proba(scaled)[0][1])
    prediction = 1 if prob >= 0.5 else 0

    # Step 4: SHAP explanation
    shap_values = explainer.shap_values(pd.DataFrame(scaled, columns=feature_columns))
    shap_series = pd.Series(shap_values[0], index=feature_columns)
    top_factors = shap_series.abs().nlargest(5).index.tolist()

    explanation = []
    for feature in top_factors:
        impact = round(float(shap_series[feature]), 4)
        explanation.append({
            "feature": feature,
            "impact": impact,
            "message": f"{'Increased' if impact > 0 else 'Decreased'} default risk"
        })

    return {
        "default_probability": round(prob, 4),
        "prediction": prediction,
        "risk_label": "HIGH RISK" if prediction == 1 else "LOW RISK",
        "shap_explanation": explanation
    }