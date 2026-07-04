import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

companies = pd.read_sql("""
SELECT DISTINCT company_id
FROM financial_ratios
ORDER BY company_id
""", conn)

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

df = pd.read_sql(f"""
SELECT *
FROM financial_ratios
WHERE company_id='{company}'
""", conn)

st.dataframe(df, use_container_width=True)

conn.close()