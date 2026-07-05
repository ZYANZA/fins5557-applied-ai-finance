
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="FINS5557 Credit Risk Dashboard",
    layout="wide",
)

@st.cache_resource
def load_model():
    with open("credit_pipeline.pkl", "rb") as f:
        return pickle.load(f)

pipeline = load_model()

ALL_FEAT = ["credit_score","income_k","employment_years","debt_to_income",
            "num_credit_lines","previous_defaults","loan_amount_k",
            "util_payment_score","rental_months","tx_velocity",
            "balance_stability","gig_income_pct","digital_engagement"]

# ---- Sidebar: applicant inputs ----
st.sidebar.header("Applicant Profile")
credit_score     = st.sidebar.slider("Credit Score",            300, 850, 680)
income_k         = st.sidebar.slider("Annual Income (AUD K)",    25, 500,  80)
employment_years = st.sidebar.slider("Employment Years",          0,  40,   5)
debt_to_income   = st.sidebar.slider("Debt-to-Income Ratio",   0.0, 0.8, 0.25, step=0.01)
num_credit_lines = st.sidebar.slider("Number of Credit Lines",   0,  15,   3)
previous_defaults= int(st.sidebar.selectbox("Previous Defaults", ["No (0)","Yes (1)"]).startswith("Y"))
loan_amount_k    = st.sidebar.slider("Loan Amount (AUD K)",       1, 200,  30)
util_pay         = st.sidebar.slider("Utility Payment Score",   0.0, 1.0, 0.8, step=0.01)
rental_months    = float(st.sidebar.slider("Rental Payment History (months)", 0, 72, 24))
tx_velocity      = float(st.sidebar.slider("Transaction Velocity (per month)", 1, 200, 45))
balance_stability= st.sidebar.slider("Balance Stability",       0.0, 1.0, 0.6, step=0.01)
gig_income_pct   = st.sidebar.slider("Gig Income Proportion",  0.0, 0.6, 0.05, step=0.01)
digital_engagement = st.sidebar.slider("Digital Engagement",   0.0, 1.0, 0.7, step=0.01)

features = np.array([[credit_score, income_k, employment_years, debt_to_income,
                       num_credit_lines, previous_defaults, loan_amount_k,
                       util_pay, rental_months, tx_velocity,
                       balance_stability, gig_income_pct, digital_engagement]])

prob     = pipeline.predict_proba(features)[0][1]
decision = "APPROVED" if prob < 0.35 else "DECLINED"
colour   = "#1A7A4A" if decision == "APPROVED" else "#C8102E"

# ---- Main panel ----
st.title("Credit Risk Scoring Dashboard")
st.markdown("**FINS5557 Applied AI in Finance | UNSW Business School | Hric & Lin, 2026**")
st.divider()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric("P(Default)", f"{prob:.1%}")
with col2:
    st.metric("Decision Threshold", "35%")
with col3:
    badge = (
        f'<div style="background:{colour};padding:14px;border-radius:8px;'
        f'text-align:center;color:white;font-size:1.5em;font-weight:bold;">'
        f'{decision}</div>'
    )
    st.markdown(badge, unsafe_allow_html=True)

st.divider()

# Feature importance bar
feat_df = pd.DataFrame({"Feature": ALL_FEAT, "Input Value": features[0]})
st.subheader("Applicant Feature Summary")
st.dataframe(feat_df.set_index("Feature").T.round(3))

# Model Card
with st.expander("Model Card (SR 11-7 Documentation)"):
    st.markdown(
        "- **Model type:** GradientBoostingClassifier (sklearn Pipeline)\n"
        "- **Features:** 7 traditional bureau + 6 alternative data\n"
        "- **Training data:** 10,000 synthetic applicants (FINS5557, seed=2025)\n"
        "- **Performance:** AUC approx 0.84, Gini approx 0.68\n"
        "- **Decision threshold:** 0.35\n"
        "- **Regulatory anchors:** SR 11-7, ASIC RG 255, NCA s124, Privacy Act 1988"
    )
