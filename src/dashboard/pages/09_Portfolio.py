import streamlit as st
from pathlib import Path

st.title("📊 Portfolio Summary")

pdf = Path("reports/portfolio/portfolio_summary.pdf")

if pdf.exists():

    st.success("Portfolio Summary Report Available")

    with open(pdf, "rb") as f:

        st.download_button(

            "📥 Download Portfolio Summary",

            f,

            file_name="portfolio_summary.pdf",

            mime="application/pdf"

        )

else:

    st.error("Portfolio Summary PDF not found.")