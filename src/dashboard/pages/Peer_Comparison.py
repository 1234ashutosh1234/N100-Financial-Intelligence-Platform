import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Peer Percentiles")

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql(
    """
    SELECT *
    FROM peer_percentiles
    """,
    conn
)

st.metric("Rows", len(df))

st.dataframe(
    df,
    use_container_width=True
)

conn.close()