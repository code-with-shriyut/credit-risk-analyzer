import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Prediction Result", page_icon="📊", layout="centered")

# redirect if not logged in
if "token" not in st.session_state:
    st.warning("Please login first!")
    st.switch_page("app.py")

# redirect if no result
if "result" not in st.session_state:
    st.warning("No application submitted!")
    st.switch_page("pages/1_Loan_Form.py")

result = st.session_state["result"]

st.title("📊 Prediction Result")
st.divider()

# Decision banner
decision = result["decision"]
risk = result["risk_category"]
prob = result["default_probability"]

if decision == "APPROVED":
    st.success(f"✅ APPROVED — {risk}")
else:
    st.error(f"❌ REJECTED — {risk}")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Decision", decision)
col2.metric("Risk Category", risk)
col3.metric("Default Probability", f"{prob*100:.1f}%")

st.caption(f"Application ID: {result['application_id']} | Processed by: {result['processed_by']} | {result['timestamp'][:19]}")

st.divider()

# SHAP explanation
st.subheader("🔍 Why this decision?")

shap_data = result.get("shap_explanation", [])

if shap_data:
    features = [s["feature"] for s in shap_data]
    impacts = [s["impact"] for s in shap_data]
    colors = ["red" if i > 0 else "green" for i in impacts]

    fig = go.Figure(go.Bar(
        x=impacts,
        y=features,
        orientation="h",
        marker_color=colors
    ))

    fig.update_layout(
        title="Top 5 Factors Affecting Decision",
        xaxis_title="Impact on Default Risk",
        yaxis_title="Feature",
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Factor Details")
    for s in shap_data:
        icon = "🔴" if s["impact"] > 0 else "🟢"
        st.write(f"{icon} **{s['feature']}** — {s['message']} (impact: {s['impact']:.4f})")

st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("New Application", use_container_width=True):
        del st.session_state["result"]
        st.switch_page("pages/1_Loan_Form.py")
with col2:
    if st.button("View Dashboard", use_container_width=True):
        st.switch_page("pages/3_Dashboard.py")
        