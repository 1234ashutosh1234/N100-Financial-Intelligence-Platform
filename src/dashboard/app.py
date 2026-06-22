import streamlit as st

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    layout="wide"
)

st.title("📈 N100 Financial Intelligence Platform")

st.write("Sprint 2 Setup Completed Successfully")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Companies", "100")
col2.metric("Top Sector", "IT")
col3.metric("Top Stock", "TCS")
col4.metric("Health Score", "95")