import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⭐ Investment Recommendations")

df = pd.read_csv(
    "output/top_recommendations.csv"
)

st.dataframe(
    df.head(20),
    width="stretch"
)

fig = px.bar(
    df.head(10),
    x="company_id",
    y="score",
    title="Top Recommended Stocks"
)

st.plotly_chart(
    fig,
    width="stretch"
)