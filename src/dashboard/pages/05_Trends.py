import streamlit as st
import plotly.express as px

from dashboard.utils.db import get_ratios

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

st.title("📈 Trend Analysis Dashboard")

# -----------------------------------
# Load Data
# -----------------------------------

df = get_ratios()

# Convert year like "Mar 2022" -> 2022
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

# -----------------------------------
# KPI Cards
# -----------------------------------

c1, c2, c3 = st.columns(3)

latest = company_df.iloc[-1]

c1.metric(
    "Latest ROE",
    f"{latest['return_on_equity_pct']:.2f}%"
)

c2.metric(
    "Latest ROCE",
    f"{latest['roce_pct']:.2f}%"
)

c3.metric(
    "Growth Score",
    int(latest["growth_score"])
)

st.divider()

# -----------------------------------
# Revenue CAGR
# -----------------------------------

st.subheader("Revenue CAGR Trend")

fig = px.line(
    company_df,
    x="year_num",
    y="sales_cagr_pct",
    markers=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# -----------------------------------
# Profit CAGR
# -----------------------------------

st.subheader("Profit CAGR Trend")

fig = px.line(
    company_df,
    x="year_num",
    y="profit_cagr_pct",
    markers=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# -----------------------------------
# EPS CAGR
# -----------------------------------

st.subheader("EPS CAGR Trend")

fig = px.line(
    company_df,
    x="year_num",
    y="eps_cagr_pct",
    markers=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# -----------------------------------
# Growth Score
# -----------------------------------

st.subheader("Growth Score Trend")

fig = px.bar(
    company_df,
    x="year_num",
    y="growth_score",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# -----------------------------------
# ROE Trend
# -----------------------------------

st.subheader("ROE Trend")

fig = px.line(
    company_df,
    x="year_num",
    y="return_on_equity_pct",
    markers=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# -----------------------------------
# ROCE Trend
# -----------------------------------

st.subheader("ROCE Trend")

fig = px.line(
    company_df,
    x="year_num",
    y="roce_pct",
    markers=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.success("Trend Dashboard Loaded Successfully")