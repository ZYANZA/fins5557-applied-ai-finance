import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="FINS5557 Super Fund Planner | UNSW", layout="wide")

SG_RATE = 0.115; CONTR_TAX = 0.15; INFLATION = 0.025
ASFA_COMFORTABLE_SINGLE = 51_630; ASFA_COMFORTABLE_COUPLE = 72_148
SUPER_ASSETS = ["Equities (Aust.)", "Equities (Intl.)", "Property", "Bonds", "Cash"]
BASE_ALLOCS = {
    "Conservative": {"Equities (Aust.)": 0.10, "Equities (Intl.)": 0.10,
                     "Property": 0.05, "Bonds": 0.60, "Cash": 0.15},
    "Balanced":     {"Equities (Aust.)": 0.25, "Equities (Intl.)": 0.25,
                     "Property": 0.10, "Bonds": 0.30, "Cash": 0.10},
    "Growth":       {"Equities (Aust.)": 0.35, "Equities (Intl.)": 0.30,
                     "Property": 0.15, "Bonds": 0.15, "Cash": 0.05},
    "High Growth":  {"Equities (Aust.)": 0.42, "Equities (Intl.)": 0.38,
                     "Property": 0.10, "Bonds": 0.08, "Cash": 0.02},
}
ASSET_MU    = {"Equities (Aust.)": 0.088, "Equities (Intl.)": 0.092,
               "Property": 0.074, "Bonds": 0.040, "Cash": 0.043}
ASSET_SIGMA = {"Equities (Aust.)": 0.155, "Equities (Intl.)": 0.168,
               "Property": 0.135, "Bonds": 0.058, "Cash": 0.008}
NAVY="#003366"; RED="#C8102E"; GREEN="#1A7A4A"; ORANGE="#D4820A"; PURPLE="#6B21A8"
COLOURS=[NAVY,RED,GREEN,ORANGE,PURPLE]

def glide_path_alloc(age, profile):
    base = {k: v for k, v in BASE_ALLOCS[profile].items()}
    if age > 50:
        reduction = min((age - 50) * 0.008, 0.20)
        base["Equities (Aust.)"] = max(base["Equities (Aust.)"] - reduction * 0.5, 0.05)
        base["Equities (Intl.)"] = max(base["Equities (Intl.)"] - reduction * 0.5, 0.05)
        base["Bonds"] += reduction * 0.60; base["Cash"] += reduction * 0.40
    total = sum(base.values())
    return {k: v/total for k, v in base.items()}

@st.cache_data
def simulate_accumulation(current_age, retire_age, balance, salary, emp_pct, vol_pct, profile, seed=42):
    np.random.seed(seed); n_years = retire_age - current_age
    paths = np.zeros((2000, n_years+1)); paths[:,0] = balance
    for t in range(n_years):
        alloc = glide_path_alloc(current_age+t, profile)
        mu_t  = sum(alloc[a]*ASSET_MU[a] for a in SUPER_ASSETS)
        sig_t = sum(alloc[a]*ASSET_SIGMA[a] for a in SUPER_ASSETS)*0.85
        r_t   = np.random.normal(mu_t, sig_t, 2000)
        contr = salary*(emp_pct+vol_pct)*(1-CONTR_TAX)*(1+INFLATION)**t
        paths[:,t+1] = paths[:,t]*(1+r_t)+contr
    return paths

# ── Sidebar ──
st.sidebar.header("Member Profile")
current_age     = st.sidebar.slider("Current Age", 20, 60, 35)
retire_age      = st.sidebar.slider("Target Retirement Age", 55, 70, 67)
current_balance = st.sidebar.number_input("Current Super Balance (AUD)", 0, 2_000_000, 85_000, 5_000)
salary          = st.sidebar.number_input("Annual Salary (AUD)", 30_000, 500_000, 110_000, 5_000)
vol_pct         = st.sidebar.slider("Extra Voluntary Contributions (%)", 0.0, 0.15, 0.0, 0.01)
profile         = st.sidebar.selectbox("Investment Option", list(BASE_ALLOCS.keys()), index=2)
couple          = st.sidebar.checkbox("Planning for a couple?", value=False)
asfa_target     = ASFA_COMFORTABLE_COUPLE if couple else ASFA_COMFORTABLE_SINGLE

paths = simulate_accumulation(current_age, retire_age, current_balance,
                               salary, SG_RATE, vol_pct, profile)
n_years = retire_age - current_age
ages = np.arange(current_age, retire_age+1)
p10,p25,p50,p75,p90 = np.percentile(paths,[10,25,50,75,90],axis=0)
median_retire = np.median(paths[:,-1])
withdrawal    = asfa_target * (1+INFLATION)**(retire_age-current_age)
coverage_ratio = median_retire*0.04 / withdrawal

# ── Main panel ──
st.title("FINS5557 Superannuation Retirement Planner")
st.markdown("**UNSW Business School | Hric & Lin, 2026 | APRA SPS 515/530 Compliant**")
st.divider()

col1,col2,col3,col4 = st.columns(4)
col1.metric("Projected Balance (Median)", f"AUD {median_retire/1e6:.2f}M")
col2.metric("ASFA Comfortable Target", f"AUD {asfa_target:,}/yr")
col3.metric("Safe Withdrawal Rate", "4.0% p.a.")
col4.metric("Coverage Ratio", f"{coverage_ratio:.2f}x",
            delta=f"{'Surplus' if coverage_ratio>=1 else 'Shortfall'}")

st.divider()

fig, axes = plt.subplots(1,2,figsize=(14,5))
# Fan chart
axes[0].fill_between(ages,p10/1e6,p90/1e6,alpha=0.15,color=NAVY,label="p10–p90")
axes[0].fill_between(ages,p25/1e6,p75/1e6,alpha=0.30,color=RED, label="p25–p75")
axes[0].plot(ages,p50/1e6,color=NAVY,lw=2,label="Median")
axes[0].axhline(asfa_target*25/1e6,color=GREEN,linestyle="--",lw=1.5,
                label=f"ASFA 25yr: AUD {asfa_target*25/1e6:.2f}M")
axes[0].set_xlabel("Age"); axes[0].set_ylabel("Balance (AUD M)")
axes[0].set_title(f"Accumulation Projection — {profile}"); axes[0].legend(fontsize=8)
# Glide path
milestones=[current_age]+list(range(max(current_age+5,50),retire_age+1,5))[:5]+[retire_age]
milestones=sorted(set(milestones))
x=np.arange(len(milestones)); w=0.16
for j,asset in enumerate(SUPER_ASSETS):
    vals=[glide_path_alloc(a,profile)[asset]*100 for a in milestones]
    axes[1].bar(x+j*w,vals,w,label=asset,color=COLOURS[j],alpha=0.85)
axes[1].set_xticks(x+w*2); axes[1].set_xticklabels([f"Age {a}" for a in milestones],fontsize=8,rotation=15)
axes[1].set_ylabel("Allocation (%)"); axes[1].set_title(f"Lifecycle Glide Path — {profile}")
axes[1].legend(fontsize=7)
st.pyplot(fig)

# Sensitivity table
rows=[]
for extra in [0.0,0.02,0.05,0.08,0.10,0.15]:
    p=simulate_accumulation(current_age,retire_age,current_balance,salary,SG_RATE,extra,profile)
    m=np.median(p[:,-1]); rows.append({"Extra Contribution":f"{extra:.0%}","Median Balance":f"AUD {m/1e6:.3f}M","Coverage Ratio":f"{m*0.04/withdrawal:.2f}x"})
st.subheader("Voluntary Contribution Sensitivity")
st.dataframe(pd.DataFrame(rows),hide_index=True)

with st.expander("APRA SPS 515 Model Card"):
    st.markdown(
        "- **Regulatory basis:** APRA SPS 515 (member outcomes), SPS 530 (investment governance), SIS Act 1993\n"
        "- **Methodology:** Monte Carlo (2,000 paths), Cholesky-free normal approximation, lifecycle glide path\n"
        "- **Glide path rule:** equity allocation reduces 0.8%/yr above age 50, max 20pp total reduction\n"
        "- **ASFA benchmark:** comfortable retirement AUD 51,630/yr (single, 2024-25)\n"
        "- **Limitations:** assumes normal return distribution; excludes death/disability, tax optimisation\n"
        "- **Data:** synthetic projections for educational purposes only — not personal financial advice"
    )
