import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_company_profile,
    get_ratios,
    get_sectors,
)

st.set_page_config(layout="wide")

st.title("🏢 Company Profile")

companies = get_company_profile()
ratios = get_ratios()
sectors = get_sectors()

company = st.selectbox(
    "Select Company",
    sorted(companies["id"].unique())
)

profile = companies[
    companies["id"] == company
].iloc[0]

st.subheader(profile["company_name"])

col1, col2 = st.columns(2)

with col1:

    st.write("### Company Information")

    st.write("Website:", profile["website"])

    st.write("Book Value:", profile["book_value"])

    st.write("ROE:", profile["roe_percentage"])

    st.write("ROCE:", profile["roce_percentage"])

with col2:

    sector = sectors[
        sectors["company_id"] == company
    ]

    if len(sector):

        st.write("### Sector")

        st.write(
            "Broad Sector:",
            sector.iloc[0]["broad_sector"]
        )

        st.write(
            "Sub Sector:",
            sector.iloc[0]["sub_sector"]
        )

company_ratio = ratios[
    ratios["company_id"] == company
].copy()

company_ratio["year_num"] = (
    company_ratio["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

company_ratio = company_ratio.sort_values(
    "year_num"
)

st.divider()

st.subheader("ROE Trend")

fig = px.line(
    company_ratio,
    x="year_num",
    y="return_on_equity_pct",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("ROCE Trend")

fig = px.line(
    company_ratio,
    x="year_num",
    y="roce_pct",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)