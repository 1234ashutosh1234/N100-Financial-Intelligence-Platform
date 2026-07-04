import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM company_rankings
ORDER BY overall_rank
""", conn)

st.title("Company Rankings")

st.dataframe(df, use_container_width=True)

conn.close()