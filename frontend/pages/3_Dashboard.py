import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://credit-risk-analyzer-3-nhhn.onrender.com"

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

if "token" not in st.session_state:
    st.warning("Please login first!")
    st.switch_page("app.py")

st.title("📈 Bank Manager Dashboard")
st.caption(f"Logged in as: {st.session_state.get('username', '')} | Role: {st.session_state.get('role', '')}")
st.divider()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}
response = requests.get(f"{API_URL}/applications", headers=headers)

if response.status_code == 200:
    data = response.json()
    applications = data["applications"]
    total = data["total"]
    df = pd.DataFrame(applications)

    # stats
    approved = len(df[df["decision"] == "APPROVED"])
    rejected = len(df[df["decision"] == "REJECTED"])
    approval_rate = round((approved / total) * 100, 1) if total > 0 else 0
    avg_prob = round(df["default_probability"].mean() * 100, 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Applications", total)
    col2.metric("Approved", approved)
    col3.metric("Approval Rate", f"{approval_rate}%")
    col4.metric("Avg Default Probability", f"{avg_prob}%")

    st.divider()

    # charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Decision Distribution")
        decision_counts = df["decision"].value_counts().reset_index()
        decision_counts.columns = ["Decision", "Count"]
        fig1 = px.pie(decision_counts, names="Decision", values="Count",
                     color_discrete_map={"APPROVED": "green", "REJECTED": "red"})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Risk Category Distribution")
        risk_counts = df["risk_category"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]
        fig2 = px.bar(risk_counts, x="Risk", y="Count",
                     color="Risk", color_discrete_map={
                         "LOW RISK": "green",
                         "MEDIUM RISK": "orange",
                         "HIGH RISK": "red"
                     })
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("All Applications")
    st.dataframe(df, use_container_width=True)

else:
    st.error("Failed to fetch applications!")

st.divider()
if st.button("New Application", use_container_width=True):
    st.switch_page("pages/1_Loan_Form.py")