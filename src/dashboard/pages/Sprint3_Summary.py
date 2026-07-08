import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Sprint 3 Summary", layout="wide")

st.title("🚀 Sprint 3 Summary")

conn = sqlite3.connect("data/nifty100.db")

ratios = pd.read_sql("SELECT COUNT(*) cnt FROM financial_ratios", conn)
peer = pd.read_sql("SELECT COUNT(*) cnt FROM peer_percentiles", conn)

st.metric("Financial Ratios", int(ratios.iloc[0]["cnt"]))
st.metric("Peer Rankings", int(peer.iloc[0]["cnt"]))

st.success("Sprint 3 Analytics Completed Successfully")

conn.close()