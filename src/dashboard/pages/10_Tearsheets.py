import streamlit as st
from pathlib import Path

st.title("📄 Company Tearsheets")

folder = Path("reports/tearsheets")

pdfs = sorted(folder.glob("*.pdf"))

if not pdfs:

    st.error("No tearsheets found.")

else:

    names = [p.stem for p in pdfs]

    selected = st.selectbox(

        "Select Company",

        names

    )

    pdf = folder / f"{selected}.pdf"

    with open(pdf, "rb") as f:

        st.download_button(

            "Download PDF",

            f,

            file_name=pdf.name,

            mime="application/pdf"

        )