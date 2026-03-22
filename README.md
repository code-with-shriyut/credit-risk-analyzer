# 🏦 Credit Risk Analyzer

> An enterprise-grade loan default prediction system built with FastAPI, XGBoost, SHAP, and Streamlit — designed for real-world banking use cases.

---

## 📌 Problem Statement

Over **190 million thin-file borrowers** in India lack formal credit history, making them invisible to traditional credit scoring systems. This project addresses **credit invisibility** by building an ML-powered loan default prediction system that uses alternative data sources (external scores, employment history, asset ownership) to evaluate creditworthiness — enabling fairer, data-driven lending decisions.

---

## 🚀 Features

- **JWT Authentication** — Secure login system for bank officers with role-based access
- **XGBoost Prediction** — Trained on Home Credit Default Risk dataset (200+ features)
- **SHAP Explainability** — Every decision comes with a reason (regulatory compliance)
- **Hybrid Decision Engine** — Rule-based filter + ML model for reliable decisions
- **Audit Trail** — Every application logged to PostgreSQL (Supabase)
- **Streamlit Dashboard** — Real-time analytics for bank managers
- **REST API** — FastAPI with auto-generated Swagger documentation


---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| ML Model | XGBoost (ROC-AUC: 0.7601) |
| Explainability | SHAP TreeExplainer |
| Authentication | JWT + bcrypt |
| Database | PostgreSQL via Supabase |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Visualization | Plotly |


---

## 📁 Project Structure
```
credit-risk-analyzer/
├── src/
│   ├── main.py           # FastAPI app — all endpoints
│   ├── auth.py           # JWT authentication
│   ├── db.py             # Database connection (Supabase)
│   ├── ml_model.py       # XGBoost + SHAP prediction
│   ├── risk.py           # Rule-based engine
│   ├── schemas.py        # Pydantic models
│   └── decision.py       # Decision logic
├── pages/
│   ├── 1_Loan_Form.py    # Loan application form
│   ├── 2_Result.py       # Prediction result + SHAP chart
│   └── 3_Dashboard.py    # Bank manager dashboard
├── tests/
│   ├── test_auth.py      # Auth function tests
│   ├── test_risk.py      # Rule engine tests
│   └── test_ml_model.py  # Model output tests
├── notebooks/
│   ├── 01_eda_home_credit.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_ml_model.ipynb
│   └── 04_shap_explain.ipynb
├── models/               # Saved model artifacts
│   ├── xgb_model.pkl
│   ├── scaler.pkl
│   └── feature_columns.pkl
├── app.py                # Streamlit entry point (login)
├── requirements.txt
└── .env                  # Environment variables (not tracked)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/code-with-shriyut/credit-risk-analyzer.git
cd credit-risk-analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=your_database_url
```

### 5. Run FastAPI backend
```bash
uvicorn src.main:app --reload
```

### 6. Run Streamlit frontend
```bash
streamlit run app.py
```

### 7. Run Tests
```bash
pytest tests/ -v
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/health` | API health check | No |
| POST | `/login` | Get JWT token | No |
| POST | `/predict` | Loan default prediction | Yes |
| GET | `/applications` | All loan applications | Yes |

### Sample `/predict` request
```json
{
  "full_name": "Rahul Sharma",
  "gender": "M",
  "age_years": 35,
  "AMT_INCOME_TOTAL": 150000,
  "AMT_CREDIT": 500000,
  "AMT_ANNUITY": 25000,
  "DAYS_BIRTH": -12775,
  "DAYS_EMPLOYED": -2000,
  "EXT_SOURCE_1": 0.6,
  "EXT_SOURCE_2": 0.7,
  "EXT_SOURCE_3": 0.5,
  "CODE_GENDER": 1,
  "FLAG_OWN_CAR": 1,
  "FLAG_OWN_REALTY": 1
}
```

### Sample response
```json
{
  "application_id": "8235BBC6",
  "decision": "APPROVED",
  "risk_category": "LOW RISK",
  "default_probability": 0.0801,
  "processed_by": "admin",
  "shap_explanation": [
    {
      "feature": "EXT_SOURCE_2",
      "impact": -0.6752,
      "message": "Decreased default risk"
    }
  ]
}
```

---

## 🤖 ML Model

- **Dataset**: Home Credit Default Risk (Kaggle)
- **Training samples**: 307,511 loan applications
- **Features**: 200+ engineered features
- **Algorithm**: XGBoost Classifier
- **ROC-AUC**: 0.7601
- **Class imbalance**: Handled via `scale_pos_weight`

### Understanding ROC-AUC 0.7601

The Home Credit dataset has severe class imbalance — **91.9% non-default, 8.1% default**. In this context, raw accuracy is misleading (a model predicting "no default" for everyone would score 91.9% accuracy but be useless).

ROC-AUC of **0.7601 after handling class imbalance** is meaningful because:
- It measures the model's ability to distinguish defaulters from non-defaulters across all thresholds
- Industry benchmark for similar thin-file credit scoring models: **0.72–0.80**
- Our model sits within the industry range without access to bureau data or transaction history

### Decision Logic (Hybrid Approach)
```
Rule Engine → HIGH RISK   → REJECTED (fast filter)
Rule Engine → LOW RISK    → ML probability < 0.3 → APPROVED
Rule Engine → MEDIUM RISK → ML model decides
```

ML model always runs for audit trail and SHAP explanation, even when rule engine makes the final call.

---

## 📊 SHAP Explainability

Every prediction includes a SHAP explanation — showing which features influenced the decision and by how much. This ensures:
- **Regulatory compliance** — RBI requires loan rejection reasons
- **Transparency** — Loan officers understand every decision
- **Fairness** — No black-box decisions

Top influencing features per prediction are returned with direction (increased/decreased risk) and magnitude.

---

## 🗄️ Database Schema
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Loan applications audit trail
CREATE TABLE loan_applications (
    id SERIAL PRIMARY KEY,
    application_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    decision VARCHAR(20),
    risk_category VARCHAR(20),
    default_probability FLOAT,
    processed_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Security

- Passwords hashed with **bcrypt** — never stored in plain text
- **JWT tokens** expire after 30 minutes
- Environment variables for all sensitive credentials
- `.env` file excluded from version control

---

## ⚠️ Known Limitations

- ROC-AUC of 0.7601 is within industry range but can be improved with hyperparameter tuning (Optuna) and advanced feature selection
- No refresh token — users must re-login every 30 minutes
- No token blacklist — logout is client-side only
- Single admin user — no registration endpoint yet
- Dataset from 2018 — may not reflect current lending patterns

---

## 📈 Future Improvements

- [ ] Hyperparameter tuning with Optuna (target ROC-AUC 0.80+)
- [ ] Refresh token implementation
- [ ] Token blacklist for secure logout
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions
- [ ] Model drift monitoring

---

## 👩‍💻 Author

**Shriyut** — B.Tech CSE, Asansol Engineering College
