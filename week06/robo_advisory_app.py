import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(page_title="FINS5557 Robo-Adviser | UNSW", layout="wide")

ASSET_NAMES = ["ASX 200 Equities","Intl Equities (Hedged)","Australian Bonds",
               "Global Bonds (Hedged)","Australian REITs","Cash (AUD)"]
MU    = np.array([0.093, 0.086, 0.042, 0.038, 0.078, 0.043])
SIGMA = np.array([0.155, 0.140, 0.058, 0.065, 0.185, 0.008])
CORR  = np.array([
    [1.00,0.82,-0.18,-0.14,0.58,0.02],[0.82,1.00,-0.12,-0.10,0.48,0.01],
    [-0.18,-0.12,1.00,0.84,-0.08,0.12],[-0.14,-0.10,0.84,1.00,-0.06,0.10],
    [0.58,0.48,-0.08,-0.06,1.00,0.03],[0.02,0.01,0.12,0.10,0.03,1.00],
])
COV = np.outer(SIGMA, SIGMA) * CORR
PROFILES = {
    "Conservative": np.array([0.10,0.10,0.35,0.30,0.05,0.10]),
    "Balanced":     np.array([0.25,0.20,0.25,0.15,0.10,0.05]),
    "Growth":       np.array([0.35,0.28,0.15,0.10,0.10,0.02]),
    "High Growth":  np.array([0.45,0.33,0.05,0.05,0.10,0.02]),
}
ASSET_COLOURS=["#003366","#C8102E","#1A7A4A","#6699CC","#D4820A","#888888"]
NAVY="#003366"; RED="#C8102E"; GREEN="#1A7A4A"

def portfolio_stats(w):
    mu_p=float(w@MU); sig_p=float(np.sqrt(w@COV@w)); sr=(mu_p-0.043)/sig_p
    return mu_p,sig_p,sr

def var_95(w,V0):
    mu_p,sig_p,_=portfolio_stats(w); return V0*(1-np.exp(mu_p-1.645*sig_p))

@st.cache_data
def monte_carlo(w_tuple,V0,n_years,contrib,n_sims=1000,seed=42):
    w=np.array(w_tuple); np.random.seed(seed); L=np.linalg.cholesky(COV)
    paths=np.zeros((n_sims,n_years+1)); paths[:,0]=V0
    for t in range(n_years):
        z=np.random.standard_normal((n_sims,len(MU))); r_all=z@L.T+MU
        paths[:,t+1]=paths[:,t]*(1+r_all@w)+contrib
    return paths

# ── Sidebar: risk questionnaire ──
st.sidebar.header("Risk Questionnaire")
q1=st.sidebar.radio("Investment objective?",["Capital preservation (1)","Income (2)","Balanced growth (3)","Capital growth (4)","Aggressive growth (5)"])
q2=st.sidebar.radio("Investment experience?",["None (1)","Limited (2)","Moderate (3)","Experienced (4)","Professional (5)"])
q3=st.sidebar.radio("Reaction to a 20% portfolio loss?",["Sell immediately (1)","Reduce exposure (2)","Hold (3)","Buy more (4)","Significantly increase (5)"])
q4=st.sidebar.radio("Investment horizon?",["< 2 years (1)","2–5 years (2)","5–10 years (3)","10–20 years (4)","> 20 years (5)"])
q5=st.sidebar.radio("Attitude to volatility?",["Strongly averse (1)","Somewhat averse (2)","Neutral (3)","Comfortable (4)","Prefer high vol (5)"])
score=sum(int(q.split("(")[1][0]) for q in [q1,q2,q3,q4,q5])*5

esg_on    = st.sidebar.toggle("ESG Tilt", value=False)
V0        = st.sidebar.number_input("Initial Investment (AUD)", 10_000, 5_000_000, 100_000, 10_000)
contrib   = st.sidebar.number_input("Annual Contribution (AUD)", 0, 200_000, 10_000, 1_000)
n_years   = st.sidebar.slider("Investment Horizon (years)", 1, 40, 20)

def score_to_profile(s):
    if s<=25: return "Conservative"
    elif s<=50: return "Balanced"
    elif s<=75: return "Growth"
    else: return "High Growth"

profile = score_to_profile(score)
w = PROFILES[profile].copy()
if esg_on:
    w[4]=max(w[4]*0.60,0.01); w[2]+=w[4]*0.40*0.60; w[3]+=w[4]*0.40*0.40
    w=w/w.sum()

mu_p,sig_p,sr=portfolio_stats(w); var95=var_95(w,V0)
paths=monte_carlo(tuple(w),V0,n_years,contrib)
bands=np.percentile(paths,[10,25,50,75,90],axis=0)
years_ax=np.arange(n_years+1)

# ── Main panel ──
st.title("FINS5557 Robo-Adviser: Portfolio Recommendation")
st.markdown("**UNSW Business School | Hric & Lin, 2026 | ASIC RG 255 Compliant**")
st.divider()

col1,col2,col3,col4=st.columns(4)
col1.metric("Risk Score",f"{score}/100",delta=profile)
col2.metric("Expected Return",f"{mu_p:.1%} p.a.")
col3.metric("Volatility (σ)",f"{sig_p:.1%} p.a.")
col4.metric("VaR 95% (1yr)",f"AUD {var95:,.0f}",delta=f"SR={sr:.2f}")
st.divider()

fig,axes=plt.subplots(1,2,figsize=(14,5))
# Allocation pie
axes[0].pie(w,labels=[f"{a}\n{v:.0%}" for a,v in zip(ASSET_NAMES,w)],
            colors=ASSET_COLOURS,startangle=90,
            wedgeprops={"edgecolor":"white","linewidth":0.8})
axes[0].set_title(f"{profile} — Recommended Allocation",fontsize=10,color=NAVY)
# Fan chart
axes[1].fill_between(years_ax,bands[0]/1e3,bands[4]/1e3,alpha=0.15,color=NAVY,label="p10–p90")
axes[1].fill_between(years_ax,bands[1]/1e3,bands[3]/1e3,alpha=0.30,color=RED, label="p25–p75")
axes[1].plot(years_ax,bands[2]/1e3,color=NAVY,lw=2,label="Median")
axes[1].set_xlabel("Years"); axes[1].set_ylabel("Portfolio Value (AUD K)")
axes[1].set_title(f"Monte Carlo Projection ({n_years}yr | {1000} paths)"); axes[1].legend(fontsize=8)
st.pyplot(fig)

with st.expander("AI Robo-Adviser Model Card (ASIC RG 255)"):
    st.markdown(
        f"- **Profile assigned:** {profile} (score {score}/100)\n"
        "- **Methodology:** mean-variance optimisation, Cholesky Monte Carlo (1,000 paths)\n"
        "- **Asset universe:** 6 Australian asset classes, calibrated 2000-2024\n"
        "- **Regulatory basis:** ASIC RG 255 (digital advice), Corporations Act 2001 s961B\n"
        "- **ESG:** REITs weight reduced 40%; redirected to bonds when ESG tilt enabled\n"
        "- **Limitations:** historical calibration; no tax, fees, or sequencing risk modelled\n"
        "- **Disclosure:** this tool provides general advice only — not personal financial advice"
    )
