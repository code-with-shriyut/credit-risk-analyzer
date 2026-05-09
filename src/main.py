import uuid
from datetime import datetime, timezone

from src.explainability import get_reason_codes
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.schemas import LoanApplication, PredictionResponse, Token, SHAPFactor
from src.auth import verify_password, create_access_token, decode_token
from src.db import get_db, get_user, save_loan_application
from src.ml_model import predict
from src.risk import risk_classification
from sqlalchemy import text

app = FastAPI(
    title="Credit Risk Analyzer API",
    description="XGBoost-based loan default prediction with SHAP explainability",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc)}


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # STEP 1: user fetch करो
    user = get_user(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username"
        )

    # STEP 2: mapping
    user_data = dict(user._mapping)

    hashed_password = user_data.get("hashed_password")
    username = user_data.get("username")
    role = user_data.get("role")

    # STEP 3: password verify
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    # STEP 4: token
    token = create_access_token({
        "sub": username,
        "role": role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }
@app.get("/applications")
def get_applications(
    current_user: dict = Depends(decode_token),
    db: Session = Depends(get_db)
):
    """Fetch all loan applications for dashboard."""
    result = db.execute(text("SELECT * FROM loan_applications ORDER BY created_at DESC")).fetchall()
    
    applications = []
    for row in result:
        applications.append({
            "application_id": row.application_id,
            "full_name": row.full_name,
            "decision": row.decision,
            "risk_category": row.risk_category,
            "default_probability": row.default_probability,
            "processed_by": row.processed_by,
            "created_at": str(row.created_at)
        })
    
    return {"applications": applications, "total": len(applications)}


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
    input_dict["AMT_GOODS_PRICE"] = input_dict.get("AMT_CREDIT", 0)
    monthly_income = input_dict.pop("monthly_income")
    existing_obligations = input_dict.pop("existing_obligations")

    emi = input_dict.get("AMT_ANNUITY", 0)

    # FOIR calculation
    foir = (emi + existing_obligations) / monthly_income if monthly_income > 0 else 0

    rule_reasons = []

    if foir > 0.5:
        rule_reasons.append("HIGH_FOIR")

    if monthly_income < 15000:
        rule_reasons.append("LOW_INCOME")
    # rule engine runs first
    ext_source_avg = (
        input_dict.get("EXT_SOURCE_1", 0.5) +
        input_dict.get("EXT_SOURCE_2", 0.5) +
        input_dict.get("EXT_SOURCE_3", 0.5)
    ) / 3

    rule_risk = risk_classification(
        ext_source_avg=ext_source_avg,
        days_employed=input_dict.get("DAYS_EMPLOYED", -365),
        amt_annuity=emi,
        amt_income_total=input_dict.get("AMT_INCOME_TOTAL", 1),
        days_birth=input_dict.get("DAYS_BIRTH", -10000),
        foir=foir,
    )
    # ml model always runs for audit + SHAP
    result = predict(input_dict)
    reason_codes = get_reason_codes(result["shap_values"])
    reason_codes = rule_reasons + reason_codes

    if rule_risk == "HIGH RISK":
        final_risk = "HIGH RISK"
        decision = "REJECTED"

    elif rule_risk == "LOW RISK" and result["default_probability"] < 0.3:
        final_risk = "LOW RISK"
        decision = "APPROVED"

    elif rule_risk == "MEDIUM RISK":
        final_risk = "MEDIUM RISK"
        decision = "APPROVED" if result["prediction"] == 0 else "REJECTED"

    else:
        # fallback (rare case)
        final_risk = result["risk_label"]
        decision = "APPROVED" if result["prediction"] == 0 else "REJECTED"
        
    application_id = str(uuid.uuid4())[:8].upper()

    save_loan_application(db, {
        "application_id": application_id,
        "full_name": full_name,
        "decision": decision,
        "risk_category": final_risk,
        "default_probability": result["default_probability"],
        "processed_by": current_user["username"],
        "reason_codes": reason_codes,
    })

    shap_factors = [SHAPFactor(**f) for f in result["shap_explanation"]]

    return PredictionResponse(
        application_id=application_id,
        timestamp = datetime.now(timezone.utc),
        decision=decision,
        risk_category=final_risk,
        default_probability=result["default_probability"],
        processed_by=current_user["username"],
        shap_explanation=shap_factors,
        foir=round(foir, 2),
    )