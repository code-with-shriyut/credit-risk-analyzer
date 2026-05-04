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

feature_columns = joblib.load(MODELS_DIR / "feature_columns.pkl")

# SHAP explainer — uses TreeExplainer for XGBoost (fast, no background data needed)
explainer = shap.TreeExplainer(model)


def predict(input_dict: dict) -> dict:

    # Step 1: Convert to DataFrame
    df = pd.DataFrame([input_dict])
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Step 2: Prediction (NO SCALER)
    prob = float(model.predict_proba(df)[0][1])
    prediction = 1 if prob >= 0.5 else 0

    # Step 3: SHAP
    shap_values = explainer.shap_values(df)

    shap_values_row = shap_values[0] if isinstance(shap_values, (list, np.ndarray)) else shap_values

    shap_series = pd.Series(shap_values_row, index=feature_columns)

    shap_dict = {
        col: float(val) for col, val in zip(feature_columns, shap_values_row)
    }

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
        "default_probability": prob,
        "prediction": prediction,
        "risk_label": "HIGH RISK" if prediction == 1 else "LOW RISK",
        "shap_explanation": explanation,
        "shap_values": shap_dict,
    }