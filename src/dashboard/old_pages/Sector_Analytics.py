import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout="wide")

st.title("📈 Stock Screener")

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

st.metric("Companies", len(df))

company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)

filtered = df[df["company_id"] == company]

st.dataframe(
    filtered,
    use_container_width=True
)

conn.close()