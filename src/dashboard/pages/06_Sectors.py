import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_sectors,
    get_ratios,
)

st.set_page_config(
    page_title="Sector Analytics",
    layout="wide"
)

st.title("🏭 Sector Analytics Dashboard")

# ---------------------------------------
# Load Data
# ---------------------------------------

sector_df = get_sectors()
ratio_df = get_ratios()

# Fix merge keys

sector_df["company_id"] = sector_df["company_id"].astype(str)
ratio_df["company_id"] = ratio_df["company_id"].astype(str)

# Merge

df = pd.merge(
    sector_df,
    ratio_df,
    on="company_id",
    how="left"
)

# ---------------------------------------
# Sector Selection
# ---------------------------------------

sector = st.selectbox(
    "Select Broad Sector",
    sorted(df["broad_sector"].dropna().unique())
)

filtered = df[
    df["broad_sector"] == sector
]

# ---------------------------------------
# KPI Cards
# ---------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    filtered["company_id"].nunique()
)

c2.metric(
    "Average ROE",
    round(
        filtered["return_on_equity_pct"].mean(),
        2
    )
)

c3.metric(
    "Average ROCE",
    round(
        filtered["roce_pct"].mean(),
        2
    )
)

c4.metric(
    "Average Growth Score",
    round(
        filtered["growth_score"].mean(),
        2
    )
)

st.divider()

# ---------------------------------------
# Bubble Chart
# ---------------------------------------

st.subheader("ROE vs ROCE")

bubble = filtered.groupby("company_id").last().reset_index()

fig = px.scatter(
    bubble,
    x="return_on_equity_pct",
    y="roce_pct",
    size="growth_score",
    hover_name="company_id",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ---------------------------------------
# Growth Score Bar Chart
# ---------------------------------------

st.subheader("Growth Score by Company")

bar = bubble.sort_values(
    "growth_score",
    ascending=False
)

fig = px.bar(
    bar,
    x="company_id",
    y="growth_score",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ---------------------------------------
# Company Table
# ---------------------------------------

st.subheader("Sector Companies")

st.dataframe(

    bubble[
        [
            "company_id",
            "sub_sector",
            "return_on_equity_pct",
            "roce_pct",
            "growth_score",
        ]
    ],

    use_container_width=True,
    hide_index=True,
)

st.success("Sector Dashboard Loaded Successfully")