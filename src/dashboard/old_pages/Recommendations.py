import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM company_recommendations
ORDER BY confidence_score DESC
""", conn)

st.title("Investment Recommendations")

st.dataframe(df, use_container_width=True)

conn.close()