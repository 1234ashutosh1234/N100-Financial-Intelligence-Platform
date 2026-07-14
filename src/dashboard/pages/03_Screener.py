import streamlit as st
import pandas as pd

from dashboard.utils.db import (
    get_ratios,
    get_market_cap,
    get_rankings,
)

st.set_page_config(
    page_title="Advanced Stock Screener",
    layout="wide"
)

st.title("📊 Advanced Stock Screener")

# -----------------------------
# Load Data
# -----------------------------

ratios = get_ratios()
market = get_market_cap()
rankings = get_rankings()

# Merge data
# ----------------------------------
# Fix merge key data types
# ----------------------------------

ratios["company_id"] = ratios["company_id"].astype(str)
market["company_id"] = market["company_id"].astype(str)

ratios["year"] = ratios["year"].astype(str)
market["year"] = market["year"].astype(str)

# Convert "Mar 2022" -> "2022"
ratios["year"] = ratios["year"].str.extract(r"(\d{4})")

# ----------------------------------
# Merge financial ratios + market cap
# ----------------------------------

df = pd.merge(
    ratios,
    market,
    on=["company_id", "year"],
    how="left"
)

df = pd.merge(
    df,
    rankings[
        [
            "company_id",
            "year",
            "overall_score",
            "overall_rank",
        ]
    ],
    on=["company_id", "year"],
    how="left"
)

rankings["company_id"] = rankings["company_id"].astype(str)
rankings["year"] = rankings["year"].astype(str)

# Convert "Mar 2022" -> "2022" if needed
rankings["year"] = rankings["year"].str.extract(r"(\d{4})").fillna(rankings["year"])

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filter Companies")

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0.0,
    50.0,
    15.0
)

roce = st.sidebar.slider(
    "Minimum ROCE (%)",
    0.0,
    60.0,
    15.0
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    5.0,
    2.0
)

growth = st.sidebar.slider(
    "Minimum Growth Score",
    0,
    3,
    1
)

pe = st.sidebar.slider(
    "Maximum PE",
    0.0,
    100.0,
    30.0
)

search = st.sidebar.text_input(
    "Search Company ID"
)

st.sidebar.divider()

st.sidebar.subheader("Preset Screeners")

preset = st.sidebar.radio(
    "Select Preset",
    [
        "Custom",
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt Free Blue Chip",
        "Turnaround Watch",
    ]
)

# -------------------------------------------------
# Preset Screeners
# -------------------------------------------------

if preset == "Quality Compounder":

    filtered = df[
        (df["return_on_equity_pct"] >= 15)
        &
        (df["roce_pct"] >= 15)
        &
        (df["debt_to_equity"] <= 1)
        &
        (df["free_cash_flow_cr"] > 0)
        &
        (df["sales_cagr_pct"] >= 10)
    ].copy()

elif preset == "Value Pick":

    filtered = df[
        (df["pe_ratio"] <= 20)
        &
        (df["pb_ratio"] <= 3)
        &
        (df["debt_to_equity"] <= 2)
        &
        (df["dividend_yield_pct"] >= 1)
    ].copy()

elif preset == "Growth Accelerator":

    filtered = df[
        (df["profit_cagr_pct"] >= 20)
        &
        (df["sales_cagr_pct"] >= 15)
        &
        (df["debt_to_equity"] <= 2)
    ].copy()

elif preset == "Dividend Champion":

    filtered = df[
        (df["dividend_yield_pct"] >= 2)
        &
        (df["free_cash_flow_cr"] > 0)
    ].copy()

elif preset == "Debt Free Blue Chip":

    filtered = df[
        (df["debt_to_equity"] <= 0.1)
        &
        (df["return_on_equity_pct"] >= 12)
    ].copy()

elif preset == "Turnaround Watch":

    filtered = df[
        (df["sales_cagr_pct"] >= 10)
        &
        (df["free_cash_flow_cr"] > 0)
    ].copy()

else:

    filtered = df[
        (df["return_on_equity_pct"] >= roe)
        &
        (df["roce_pct"] >= roce)
        &
        (df["debt_to_equity"] <= de)
        &
        (df["growth_score"] >= growth)
        &
        (
            df["pe_ratio"].fillna(9999)
            <= pe
        )
    ].copy()
# -----------------------------
# Sort
# -----------------------------

sort_option = st.sidebar.selectbox(
    "Sort By",
    [
        "Overall Score",
        "ROE",
        "ROCE",
        "Growth Score",
    ]
)

if sort_option == "Overall Score":

    filtered = filtered.sort_values(
        "overall_score",
        ascending=False
    )

elif sort_option == "ROE":

    filtered = filtered.sort_values(
        "return_on_equity_pct",
        ascending=False
    )

elif sort_option == "ROCE":

    filtered = filtered.sort_values(
        "roce_pct",
        ascending=False
    )

else:

    filtered = filtered.sort_values(
        "growth_score",
        ascending=False
    )

# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    len(filtered)
)

c2.metric(
    "Average ROE",
    round(
        filtered["return_on_equity_pct"].mean(),
        2
    ) if len(filtered) else 0
)

c3.metric(
    "Average Overall Score",
    round(
        filtered["overall_score"].mean(),
        2
    ) if len(filtered) else 0
)

st.divider()

# -----------------------------
# Results
# -----------------------------

st.subheader("Filtered Companies")

display_cols = [
    "company_id",
    "year",
    "return_on_equity_pct",
    "roce_pct",
    "debt_to_equity",
    "growth_score",
    "pe_ratio",
    "overall_score",
    "overall_rank",
]

st.dataframe(
    filtered[display_cols],
    use_container_width=True,
    hide_index=True,
)

# -----------------------------
# CSV Export
# -----------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="screener_output.csv",
    mime="text/csv",
)