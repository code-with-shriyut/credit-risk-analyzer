import streamlit as st
import requests

API_URL = "https://credit-risk-analyzer-3-nhhn.onrender.com"

st.set_page_config(
    page_title="Credit Risk Analyzer",
    page_icon="🏦",
    layout="centered"
)

# redirect if already logged in
if "token" in st.session_state:
    st.switch_page("pages/1_Loan_Form.py")

st.title("🏦 Credit Risk Analyzer")
st.subheader("Bank Login")
st.divider()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):
    if not username or not password:
        st.error("Username aur password dono required hain")
    else:
        response = requests.post(
            f"{API_URL}/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["role"] = data["role"]
            st.session_state["username"] = username
            st.success("Login successful!")
            st.switch_page("pages/1_Loan_Form.py")
        else:
            st.error("Invalid username or password")