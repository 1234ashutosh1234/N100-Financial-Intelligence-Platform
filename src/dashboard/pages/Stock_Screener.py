import streamlit as st
import pandas as pd

st.title("🔍 Stock Screener")

df = pd.read_csv(
    "output/top_recommendations.csv"
)

min_score = st.slider(
    "Minimum Score",
    0,
    100,
    20
)

filtered = df[
    df["score"] >= min_score
]

st.dataframe(
    filtered,
    width="stretch"
)