import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

# redirect if not logged in
if "token" not in st.session_state:
    st.warning("Please login first!")
    st.switch_page("app.py")

st.title("📈 Bank Manager Dashboard")
st.caption(f"Logged in as: {st.session_state.get('username', '')} | Role: {st.session_state.get('role', '')}")
st.divider()

# fetch data from supabase directly via API
headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# for now show session result if available
if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("Latest Application")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Application ID", result["application_id"])
    col2.metric("Decision", result["decision"])
    col3.metric("Risk Category", result["risk_category"])
    col4.metric("Default Probability", f"{result['default_probability']*100:.1f}%")

    st.divider()

st.subheader("Quick Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", "Coming Soon")
col2.metric("Approval Rate", "Coming Soon")
col3.metric("Avg Default Probability", "Coming Soon")

st.divider()

st.subheader("Risk Distribution")
st.info("Connect /applications endpoint to see full dashboard with charts.")

st.divider()

if st.button("New Application", use_container_width=True):
    st.switch_page("pages/1_Loan_Form.py")
    