STREAMLIT_CODE = '''
# advisory_app.py — WealthTech Financial Advisory Platform (Week 9)
# Run: streamlit run advisory_app.py

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="WealthTech Advisory Platform", layout="wide")
st.title("WealthTech Financial Advisory Platform")
st.caption("FINS5557 Week 9 | Hric & Lin, 2026 | For use by licensed financial advisers under AFSL")

with st.sidebar:
    st.header("Adviser Settings")
    adviser_id = st.text_input("Adviser ID", value="ADV_007")
    st.divider()
    st.write("**Model Governance**")
    st.write("Recommender: PSS-v2 (Eq 9.7)")
    st.write("Alpha weights: 0.40 / 0.30 / 0.20 / 0.10")
    st.write("Product shelf: 2025-Q3")
    st.write("BID floor: PSS >= 0.50")
    st.write("Validation: 2025-09-01")
    st.write("SR 11-7 status: Approved")

tab1, tab2, tab3, tab4 = st.tabs([
    "Client Profiling",
    "Product Recommendations",
    "Portfolio Allocation",
    "SOA & Compliance"
])

with tab1:
    st.subheader("Client Risk Profiling — Eq 9.6")
    col1, col2 = st.columns(2)
    with col1:
        client_name   = st.text_input("Client name", value="Sarah Chen")
        age           = st.number_input("Age", min_value=18, max_value=90, value=45)
        investable    = st.number_input("Investable assets (AUD)", value=850000, step=10000)
        income        = st.number_input("Annual income (AUD)", value=180000, step=5000)
    with col2:
        risk_tolerance = st.slider("Risk tolerance (1=Very Conservative, 5=Aggressive)", 1, 5, 3)
        horizon        = st.slider("Investment horizon (years)", 1, 40, 20)
        income_stable  = st.checkbox("Income is stable / employment-based", value=True)
        liquidity_need = st.select_slider("Liquidity need", options=["low", "medium", "high"], value="medium")

    LIQUIDITY_MAP = {"low": 1.0, "medium": 0.5, "high": 0.0}
    V = {"risk_tolerance": 0.35, "horizon_norm": 0.25, "income_stable": 0.20, "liquidity_low": 0.20}
    q = {
        "risk_tolerance": (risk_tolerance - 1) / 4,
        "horizon_norm":   min(horizon / 30.0, 1.0),
        "income_stable":  float(income_stable),
        "liquidity_low":  LIQUIDITY_MAP[liquidity_need]
    }
    crs = sum(V[k] * q[k] for k in V)
    CATS = [(0, 0.25, "Conservative"), (0.25, 0.45, "Moderate-Conservative"),
             (0.45, 0.65, "Balanced"), (0.65, 0.80, "Growth"), (0.80, 1.01, "Aggressive Growth")]
    category = next(cat for lo, hi, cat in CATS if lo <= crs < hi)

    st.metric("Client Risk Score (CRS)", f"{crs:.3f}", help="Eq 9.6")
    st.success(f"Risk Category: **{category}**")

with tab2:
    st.subheader("Product Suitability Scores — Eq 9.7")
    st.info("Connect to: scores_df filtered by client_id from notebook Station 2-3")
    st.write("Products ranked by PSS score. BID floor: PSS >= 0.50 for recommendation.")
    demo_recs = pd.DataFrame({
        "Product":    ["Vanguard Balanced Index Fund", "AustralianSuper Balanced", "iShares S&P/ASX 200 ETF"],
        "PSS":        [0.842, 0.798, 0.751],
        "Risk fit":   [0.92, 0.88, 0.75],
        "Horizon":    [1.00, 1.00, 1.00],
        "Liquidity":  [0.85, 0.60, 0.95],
        "Fee score":  [0.86, 0.72, 0.96],
        "BID gate":   [True, True, True]
    })
    st.dataframe(demo_recs, use_container_width=True)

with tab3:
    st.subheader("Proposed Strategic Asset Allocation (IPS Target Weights)")
    IPS = {
        "Conservative":          {"AU Equities": 0.10, "Intl Equities": 0.05, "Fixed Income": 0.55, "Cash": 0.25, "Alternatives": 0.05},
        "Moderate-Conservative": {"AU Equities": 0.20, "Intl Equities": 0.15, "Fixed Income": 0.40, "Cash": 0.15, "Alternatives": 0.10},
        "Balanced":              {"AU Equities": 0.30, "Intl Equities": 0.25, "Fixed Income": 0.28, "Cash": 0.07, "Alternatives": 0.10},
        "Growth":                {"AU Equities": 0.38, "Intl Equities": 0.32, "Fixed Income": 0.15, "Cash": 0.05, "Alternatives": 0.10},
        "Aggressive Growth":     {"AU Equities": 0.42, "Intl Equities": 0.38, "Fixed Income": 0.08, "Cash": 0.02, "Alternatives": 0.10},
    }
    alloc = IPS.get(category, IPS["Balanced"])
    alloc_df = pd.DataFrame.from_dict(alloc, orient="index", columns=["Weight"])
    alloc_df["Weight %"] = (alloc_df["Weight"] * 100).round(0).astype(int)
    st.bar_chart(alloc_df["Weight"])
    st.dataframe(alloc_df[["Weight %"]], use_container_width=False)

with tab4:
    st.subheader("Statement of Advice — Draft + BID Compliance")
    st.warning("This is an AI-generated draft. The licensed adviser must review, edit, and approve before delivery. The AFSL holder bears responsibility for compliance with Best Interests Duty (Corporations Act s.961B).")
    st.write("Connect to: `soa_outputs[client_id]` from notebook Station 4")
    st.text_area("SOA Draft (adviser editable)", height=300,
                  value="[SOA draft will appear here after generation — connect to notebook pipeline output]")
    st.subheader("BID Compliance Gate Results")
    bid_demo = pd.DataFrame({
        "Check":          ["Risk profile documented", "Horizon compatibility", "Fee reasonableness",
                           "Risk alignment", "Diversification", "Conflict disclosure"],
        "Type":           ["HARD", "HARD", "SOFT", "SOFT", "SOFT", "SOFT"],
        "Result":         [True, True, True, True, True, True],
        "Note":           ["Questionnaire on file", "All products within horizon",
                           "Avg fee 0.44% p.a.", "All in risk band", "3 product types", "No trailing commissions"]
    })
    st.dataframe(bid_demo, use_container_width=True)
    st.success("BID gate: PASSED — SOA generation authorised. RM sign-off required before delivery.")
    if st.button("Export Audit Trail (CSV)"):
        st.info("In production: audit_df.to_csv('asic_advice_audit_trail.csv', index=False)")
'''

with open('advisory_app.py', 'w') as f:
    f.write(STREAMLIT_CODE.strip())

print('Streamlit adviser workstation written to advisory_app.py')
print('Run: streamlit run advisory_app.py')
print()
print('Four tabs:')
print('  Tab 1 — Client Profiling:         questionnaire → CRS (Eq 9.6) + risk category')
print('  Tab 2 — Product Recommendations:  PSS scores (Eq 9.7) + component breakdown')
print('  Tab 3 — Portfolio Allocation:     IPS target-weight bar chart')
print('  Tab 4 — SOA & Compliance:         draft SOA + BID gate results + audit trail export')
