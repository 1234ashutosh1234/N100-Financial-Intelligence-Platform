import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⭐ Investment Recommendations")

df = pd.read_csv(
    "output/top_recommendations.csv"
)

st.dataframe(
    df.head(20),
    use_container_width=True
)

fig = px.bar(
    df.head(10),
    x="company_id",
    y="score",
    title="Top Recommended Stocks"
)

st.plotly_chart(
    fig,
    use_container_width=True
)