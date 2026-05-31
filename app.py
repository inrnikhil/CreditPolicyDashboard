# app.py

import streamlit as st
import numpy as np

st.title("Credit Card Policy Engine")

st.sidebar.header("Customer Inputs")

bureau_score = st.sidebar.slider(
    "Bureau Score",
    300,
    850,
    680
)

income = st.sidebar.number_input(
    "Annual Income",
    value=80000
)

dti = st.sidebar.slider(
    "DTI %",
    0,
    100,
    30
)

utilization = st.sidebar.slider(
    "Utilization %",
    0,
    100,
    30
)

past_dq = st.sidebar.number_input(
    "Past Delinquencies",
    min_value=0,
    max_value=10,
    value=0
)

trade_num = st.sidebar.number_input(
    "Additional trade lines",
    min_value=0,
    max_value=15,
    value=0
)

age = st.sidebar.slider(
    "Age",
    21,
    75,
    35
)

# PD Model

score_effect =-0.005065*(bureau_score-680)
util_effect = 0.044488*(utilization-30)
dti_effect =  0.044417*(dti-30)
dq_effect = 0.881483*past_dq
trade_effect=0.116622*trade_num
income_effect= -0.000008*income

logit = (
    -0.0704
    + score_effect
    + util_effect
    + dti_effect
    + dq_effect
    + trade_effect
    + income_effect
)

pd_prob = 1/(1+np.exp(-logit))

# Decision

if (
    bureau_score < 500
    or dti > 60
    or past_dq >= 3
    or pd_prob > 0.60
):
    decision = "DECLINE"
else:
    decision = "APPROVE"

# Risk Tier

if pd_prob <= 0.10:
    risk_tier = "Prime"
    credit_line = 15000

elif pd_prob <= 0.20:
    risk_tier = "Near Prime"
    credit_line = 8000

elif pd_prob <= 0.35:
    risk_tier = "Subprime"
    credit_line = 3000

else:
    risk_tier = "Deep Subprime"
    credit_line = 500

st.metric(
    "Probability of Default",
    f"{pd_prob:.2%}"
)

st.metric(
    "Decision",
    decision
)

st.metric(
    "Risk Tier",
    risk_tier
)

st.metric(
    "Credit Limit",
    f"${credit_line:,.0f}"
)
