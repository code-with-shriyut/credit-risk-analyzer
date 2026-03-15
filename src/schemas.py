from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class LoanApplication(BaseModel):
    full_name: str
    gender: str = Field(..., pattern="^(M|F)$")
    age_years: int = Field(..., ge=18, le=80)
    AMT_INCOME_TOTAL: float = Field(..., gt=0)
    AMT_CREDIT: float = Field(..., gt=0)
    AMT_ANNUITY: float = Field(..., gt=0)
    AMT_GOODS_PRICE: Optional[float] = 0.0
    DAYS_BIRTH: int = Field(..., lt=0)
    DAYS_EMPLOYED: int
    EXT_SOURCE_1: Optional[float] = Field(0.5, ge=0, le=1)
    EXT_SOURCE_2: Optional[float] = Field(0.5, ge=0, le=1)
    EXT_SOURCE_3: Optional[float] = Field(0.5, ge=0, le=1)
    CODE_GENDER: int = Field(..., ge=0, le=1)
    FLAG_OWN_CAR: int = Field(..., ge=0, le=1)
    FLAG_OWN_REALTY: int = Field(..., ge=0, le=1)

class SHAPFactor(BaseModel):
    feature: str
    impact: float
    message: str

class PredictionResponse(BaseModel):
    application_id: str
    timestamp: datetime
    decision: str
    risk_category: str
    default_probability: Optional[float]
    processed_by: str
    shap_explanation: Optional[list[SHAPFactor]] = None