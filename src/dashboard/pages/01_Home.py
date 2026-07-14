import streamlit as st
import plotly.express as px
import pandas as pd

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_market_cap,
    get_rankings
)

st.set_page_config(layout="wide")

st.title("🏠 N100 Financial Intelligence Platform")

companies = get_companies()
ratios = get_ratios()
market = get_market_cap()
rankings = get_rankings()

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(companies)
)

c2.metric(
    "Average ROE",
    round(ratios["return_on_equity_pct"].mean(),2)
)

c3.metric(
    "Average ROCE",
    round(ratios["roce_pct"].mean(),2)
)

c4.metric(
    "Average Overall Score",
    round(rankings["overall_score"].mean(),2)
)

st.divider()

# -------------------------------------------------
# Top Companies
# -------------------------------------------------

st.subheader("Top Companies")

top = rankings.sort_values(
    "overall_score",
    ascending=False
).head(10)

st.dataframe(
    top,
    use_container_width=True
)

# -------------------------------------------------
# ROE Distribution
# -------------------------------------------------

st.subheader("ROE Distribution")

fig = px.histogram(
    ratios,
    x="return_on_equity_pct",
    nbins=25
)

st.plotly_chart(
    fig,
    use_container_width=True
)