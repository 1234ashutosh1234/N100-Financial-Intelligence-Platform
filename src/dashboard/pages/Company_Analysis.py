import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Company Analysis",
    layout="wide"
)

st.title("📊 Company Analysis")

# Database Connection
conn = sqlite3.connect("data/nifty100.db")

try:

    # Load Company List
    companies = pd.read_sql(
        """
        SELECT DISTINCT company_id
        FROM financial_ratios
        ORDER BY company_id
        """,
        conn
    )

    selected_company = st.sidebar.selectbox(
        "Select Company",
        companies["company_id"]
    )

    # Company Data
    company_df = pd.read_sql(
        f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{selected_company}'
        ORDER BY year
        """,
        conn
    )

    st.subheader(f"📈 {selected_company} Financial Data")

    st.dataframe(
        company_df,
        width="stretch"
    )

    # Latest Metrics
    latest = company_df.tail(1)

    col1, col2, col3, col4 = st.columns(4)

    if "return_on_equity_pct" in latest.columns:
        col1.metric(
            "ROE %",
            round(float(latest["return_on_equity_pct"].iloc[0]), 2)
        )

    if "net_profit_margin_pct" in latest.columns:
        col2.metric(
            "Net Profit Margin %",
            round(float(latest["net_profit_margin_pct"].iloc[0]), 2)
        )

    if "operating_profit_margin_pct" in latest.columns:
        col3.metric(
            "Operating Margin %",
            round(float(latest["operating_profit_margin_pct"].iloc[0]), 2)
        )

    if "debt_to_equity" in latest.columns:
        col4.metric(
            "Debt/Equity",
            round(float(latest["debt_to_equity"].iloc[0]), 2)
        )

    st.divider()

    # ROE Trend
    if "return_on_equity_pct" in company_df.columns:

        st.subheader("📈 ROE Trend")

        fig1 = px.line(
            company_df,
            x="year",
            y="return_on_equity_pct",
            markers=True,
            title=f"{selected_company} Return on Equity"
        )

        st.plotly_chart(
            fig1,
            width="stretch"
        )

    # Net Profit Margin Trend
    if "net_profit_margin_pct" in company_df.columns:

        st.subheader("💰 Net Profit Margin Trend")

        fig2 = px.line(
            company_df,
            x="year",
            y="net_profit_margin_pct",
            markers=True,
            title=f"{selected_company} Net Profit Margin"
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

    # Debt to Equity
    if "debt_to_equity" in company_df.columns:

        st.subheader("🏦 Debt to Equity Ratio")

        fig3 = px.bar(
            company_df,
            x="year",
            y="debt_to_equity",
            title=f"{selected_company} Debt to Equity"
        )

        st.plotly_chart(
            fig3,
            width="stretch"
        )

    # Operating Margin
    if "operating_profit_margin_pct" in company_df.columns:

        st.subheader("📊 Operating Profit Margin")

        fig4 = px.line(
            company_df,
            x="year",
            y="operating_profit_margin_pct",
            markers=True,
            title=f"{selected_company} Operating Profit Margin"
        )

        st.plotly_chart(
            fig4,
            width="stretch"
        )

except Exception as e:

    st.error(f"Error: {e}")

finally:
    conn.close()