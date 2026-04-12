import streamlit as st
import requests

API_URL = "https://credit-risk-analyzer-3-nhhn.onrender.com"

st.set_page_config(page_title="Loan Application", page_icon="📋", layout="centered")

# redirect if not logged in
if "token" not in st.session_state:
    st.warning("Please login first!")
    st.switch_page("app.py")

st.title("📋 Loan Application Form")
st.caption(f"Logged in as: {st.session_state.get('username', '')} | Role: {st.session_state.get('role', '')}")
st.divider()

with st.form("loan_form"):
    st.subheader("Applicant Details")
    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name")
        gender = st.selectbox("Gender", ["M", "F"])
        age_years = st.number_input("Age (years)", min_value=18, max_value=80, value=30)

    with col2:
        amt_income = st.number_input("Annual Income (₹)", min_value=10000.0, value=300000.0, step=10000.0)
        amt_credit = st.number_input("Loan Amount (₹)", min_value=10000.0, value=500000.0, step=10000.0)
        amt_annuity = st.number_input("Monthly EMI (₹)", min_value=1000.0, value=25000.0, step=1000.0)

    st.subheader("Additional Details")
    col3, col4 = st.columns(2)

    with col3:
        days_employed = st.number_input("Employment (days, negative = employed)", value=-1000)
        ext_source_2 = st.slider("Credit Score 1 (0-1)", 0.0, 1.0, 0.5)
        ext_source_3 = st.slider("Credit Score 2 (0-1)", 0.0, 1.0, 0.5)

    with col4:
        flag_own_car = st.selectbox("Owns Car?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        flag_own_realty = st.selectbox("Owns Property?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        ext_source_1 = st.slider("Credit Score 3 (0-1)", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Submit Application", use_container_width=True)

if submitted:
    if not full_name:
        st.error("Full name required!")
    else:
        payload = {
            "full_name": full_name,
            "gender": gender,
            "age_years": age_years,
            "AMT_INCOME_TOTAL": amt_income,
            "AMT_CREDIT": amt_credit,
            "AMT_ANNUITY": amt_annuity,
            "AMT_GOODS_PRICE": amt_credit * 0.9,
            "DAYS_BIRTH": -(age_years * 365),
            "DAYS_EMPLOYED": days_employed,
            "EXT_SOURCE_1": ext_source_1,
            "EXT_SOURCE_2": ext_source_2,
            "EXT_SOURCE_3": ext_source_3,
            "CODE_GENDER": 1 if gender == "M" else 0,
            "FLAG_OWN_CAR": flag_own_car,
            "FLAG_OWN_REALTY": flag_own_realty
        }

        headers = {"Authorization": f"Bearer {st.session_state['token']}"}

        with st.spinner("Analyzing application..."):
            response = requests.post(f"{API_URL}/predict", json=payload, headers=headers)

        if response.status_code == 200:
            st.session_state["result"] = response.json()
            st.switch_page("pages/2_Result.py")
        else:
            st.error(f"Error: {response.text}")