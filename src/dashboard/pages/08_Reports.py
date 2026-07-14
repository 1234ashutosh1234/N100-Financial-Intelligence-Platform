import streamlit as st
import plotly.express as px

from utils.db import get_valuation

st.set_page_config(
    page_title="Valuation Dashboard",
    layout="wide"
)

st.title("💎 Valuation Dashboard")

df = get_valuation()

# -----------------------------------
# Sidebar
# -----------------------------------

flag = st.sidebar.selectbox(
    "Valuation",
    [
        "All",
        "Undervalued",
        "Fair",
        "Overvalued"
    ]
)

if flag != "All":
    df = df[df["valuation_flag"] == flag]

# -----------------------------------
# KPI Cards
# -----------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    len(df)
)

c2.metric(
    "Average PE",
    round(df["pe_ratio"].mean(),2)
)

c3.metric(
    "Average PB",
    round(df["pb_ratio"].mean(),2)
)

st.divider()

# -----------------------------------
# Bubble Chart
# -----------------------------------

st.subheader("PE vs PB")

fig = px.scatter(

    df,

    x="pe_ratio",

    y="pb_ratio",

    color="valuation_flag",

    size="market_cap_crore",

    hover_name="company_id"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Value Score
# -----------------------------------

st.subheader("Top Value Opportunities")

table = df.sort_values(
    "value_score",
    ascending=False
)

st.dataframe(

    table[
        [
            "company_id",
            "year",
            "pe_ratio",
            "pb_ratio",
            "value_score",
            "valuation_flag",
        ]
    ],

    use_container_width=True,
    hide_index=True,
)

csv = table.to_csv(index=False).encode()

st.download_button(

    "📥 Download Valuation Report",

    csv,

    "valuation_report.csv",

    "text/csv"

)