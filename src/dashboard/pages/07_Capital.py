import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import (
    get_ratios,
)

st.set_page_config(
    page_title="Capital Allocation Dashboard",
    layout="wide"
)

st.title("💰 Capital Allocation Dashboard")

# -----------------------------
# Load Data
# -----------------------------

df = get_ratios()

df["year_num"] = (
    df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)

company_df = (
    df[df["company_id"] == company]
    .sort_values("year_num")
)

latest = company_df.iloc[-1]

# -----------------------------
# Capital Allocation Score
# -----------------------------

company_df["capital_score"] = (

    company_df["return_on_equity_pct"] * 0.30 +

    company_df["roce_pct"] * 0.30 +

    company_df["free_cash_flow_cr"] * 0.20 +

    (100 - company_df["debt_to_equity"] * 20) * 0.20
)

latest = company_df.iloc[-1]

# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "ROE",
    f"{latest['return_on_equity_pct']:.2f}%"
)

c2.metric(
    "ROCE",
    f"{latest['roce_pct']:.2f}%"
)

c3.metric(
    "Free Cash Flow",
    f"{latest['free_cash_flow_cr']:.2f}"
)

c4.metric(
    "Debt / Equity",
    f"{latest['debt_to_equity']:.2f}"
)

st.divider()

# -----------------------------
# Capital Score Trend
# -----------------------------

st.subheader("Capital Allocation Score")

fig = px.line(

    company_df,

    x="year_num",

    y="capital_score",

    markers=True,

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# ROE vs ROCE
# -----------------------------

st.subheader("ROE vs ROCE")

fig = px.scatter(

    company_df,

    x="return_on_equity_pct",

    y="roce_pct",

    size="capital_score",

    hover_data=["year"]

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Free Cash Flow Trend
# -----------------------------

st.subheader("Free Cash Flow")

fig = px.bar(

    company_df,

    x="year_num",

    y="free_cash_flow_cr"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Capital Allocation Rating
# -----------------------------

score = latest["capital_score"]

if score >= 80:
    rating = "⭐⭐⭐⭐⭐ Excellent"

elif score >= 60:
    rating = "⭐⭐⭐⭐ Very Good"

elif score >= 40:
    rating = "⭐⭐⭐ Good"

elif score >= 20:
    rating = "⭐⭐ Average"

else:
    rating = "⭐ Weak"

st.divider()

st.success(f"Capital Allocation Rating : {rating}")

st.dataframe(
    company_df[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "roce_pct",
            "free_cash_flow_cr",
            "debt_to_equity",
            "capital_score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)