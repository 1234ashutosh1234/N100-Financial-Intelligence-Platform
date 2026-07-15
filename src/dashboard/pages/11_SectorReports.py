import streamlit as st
from pathlib import Path

st.title("🏭 Sector Reports")

folder = Path("reports/sector")

pdfs = sorted(folder.glob("*.pdf"))

if not pdfs:

    st.error("No sector reports found.")

else:

    names = [p.stem for p in pdfs]

    selected = st.selectbox(

        "Select Sector",

        names

    )

    pdf = folder / f"{selected}.pdf"

    with open(pdf, "rb") as f:

        st.download_button(

            "Download Sector Report",

            f,

            file_name=pdf.name,

            mime="application/pdf"

        )