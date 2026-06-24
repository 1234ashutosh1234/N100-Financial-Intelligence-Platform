import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Sector Analytics",
    layout="wide"
)

st.title("🏭 Sector Analytics")

conn = sqlite3.connect("data/nifty100.db")

try:

    sectors_df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    st.subheader("Sector Dataset")

    st.dataframe(
        sectors_df,
        width="stretch"
    )

    # Broad Sector Analysis
    sector_count = (
        sectors_df.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    st.subheader("Sector-wise Company Distribution")

    fig1 = px.bar(
        sector_count,
        x="broad_sector",
        y="Companies",
        title="Companies per Broad Sector"
    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

    st.subheader("Sector Share")

    fig2 = px.pie(
        sector_count,
        names="broad_sector",
        values="Companies"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    st.subheader("Sector Ranking")

    st.dataframe(
        sector_count.sort_values(
            "Companies",
            ascending=False
        ),
        width="stretch"
    )

    # Market Cap Distribution
    st.subheader("Market Cap Categories")

    market_cap = (
        sectors_df.groupby("market_cap_category")
        .size()
        .reset_index(name="Companies")
    )

    fig3 = px.bar(
        market_cap,
        x="market_cap_category",
        y="Companies",
        title="Market Cap Distribution"
    )

    st.plotly_chart(
        fig3,
        width="stretch"
    )

except Exception as e:

    st.error(f"Error Loading Sector Data: {e}")

finally:
    conn.close()