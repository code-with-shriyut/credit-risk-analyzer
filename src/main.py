import uuid
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.schemas import LoanApplication, PredictionResponse, Token, SHAPFactor
from src.auth import verify_password, create_access_token, decode_token
from src.db import get_db, get_user, save_loan_application
from src.ml_model import predict
from src.risk import risk_classification

app = FastAPI(
    title="Credit Risk Analyzer API",
    description="XGBoost-based loan default prediction with SHAP explainability",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow()}


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}


@app.post("/predict", response_model=PredictionResponse)
def predict_default(
    application: LoanApplication,
    current_user: dict = Depends(decode_token),
    db: Session = Depends(get_db)
):
    input_dict = application.model_dump()
    full_name = input_dict.pop("full_name")
    gender = input_dict.pop("gender")
    age_years = input_dict.pop("age_years")

    input_dict["AGE_YEARS"] = age_years
    input_dict["CODE_GENDER_M"] = 1 if gender == "M" else 0

    # rule engine runs first
    ext_source_avg = (
        input_dict.get("EXT_SOURCE_1", 0.5) +
        input_dict.get("EXT_SOURCE_2", 0.5) +
        input_dict.get("EXT_SOURCE_3", 0.5)
    ) / 3

    rule_risk = risk_classification(
        ext_source_avg=ext_source_avg,
        days_employed=input_dict.get("DAYS_EMPLOYED", -365),
        amt_annuity=input_dict.get("AMT_ANNUITY", 0),
        amt_income_total=input_dict.get("AMT_INCOME_TOTAL", 1),
        days_birth=input_dict.get("DAYS_BIRTH", -10000)
    )

    # ml model always runs for audit + SHAP
    result = predict(input_dict)

    if rule_risk == "HIGH RISK":
        final_risk = "HIGH RISK"
        decision = "REJECTED"
    elif rule_risk == "LOW RISK" and result["default_probability"] < 0.3:
        final_risk = "LOW RISK"
        decision = "APPROVED"
    else:
        final_risk = result["risk_label"]
        decision = "APPROVED" if result["prediction"] == 0 else "REJECTED"

    application_id = str(uuid.uuid4())[:8].upper()

    save_loan_application(db, {
        "application_id": application_id,
        "full_name": full_name,
        "decision": decision,
        "risk_category": final_risk,
        "default_probability": result["default_probability"],
        "processed_by": current_user["username"]
    })

    shap_factors = [SHAPFactor(**f) for f in result["shap_explanation"]]

    return PredictionResponse(
        application_id=application_id,
        timestamp=datetime.utcnow(),
        decision=decision,
        risk_category=final_risk,
        default_probability=result["default_probability"],
        processed_by=current_user["username"],
        shap_explanation=shap_factors
    )