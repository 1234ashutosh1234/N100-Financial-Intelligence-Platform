from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os

# ---------------------------------
# CREATE REPORTS FOLDER
# ---------------------------------

os.makedirs("reports", exist_ok=True)

# ---------------------------------
# LOAD DATA
# ---------------------------------

try:
    rec_df = pd.read_csv(
        "output/top_recommendations.csv"
    )
except:
    rec_df = pd.DataFrame()

try:
    audit_df = pd.read_csv(
        "output/load_audit.csv"
    )
except:
    audit_df = pd.DataFrame()

try:
    validation_df = pd.read_csv(
        "output/validation_failures.csv"
    )
except:
    validation_df = pd.DataFrame()

# ---------------------------------
# PDF SETUP
# ---------------------------------

pdf = SimpleDocTemplate(
    "reports/company_report.pdf"
)

styles = getSampleStyleSheet()

elements = []

# ---------------------------------
# TITLE PAGE
# ---------------------------------

elements.append(
    Paragraph(
        "N100 Financial Intelligence Platform",
        styles["Title"]
    )
)

elements.append(
    Paragraph(
        "Project Analytics Report",
        styles["Heading2"]
    )
)

elements.append(Spacer(1, 20))

elements.append(
    Paragraph(
        "Generated using Python, SQLite and Streamlit",
        styles["BodyText"]
    )
)

elements.append(PageBreak())

# ---------------------------------
# LOAD AUDIT SECTION
# ---------------------------------

elements.append(
    Paragraph(
        "Database Load Audit",
        styles["Heading1"]
    )
)

elements.append(Spacer(1, 10))

if not audit_df.empty:

    for _, row in audit_df.iterrows():

        text = (
            f"{row['table_name']} : "
            f"{row['row_count']} rows"
        )

        elements.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

else:

    elements.append(
        Paragraph(
            "Load Audit File Not Found",
            styles["BodyText"]
        )
    )

elements.append(PageBreak())

# ---------------------------------
# VALIDATION SECTION
# ---------------------------------

elements.append(
    Paragraph(
        "Data Validation Report",
        styles["Heading1"]
    )
)

elements.append(Spacer(1, 10))

if not validation_df.empty:

    elements.append(
        Paragraph(
            f"Total Issues Found : {len(validation_df)}",
            styles["BodyText"]
        )
    )

    for _, row in validation_df.head(20).iterrows():

        text = (
            f"{row['Issue']} : "
            f"{row['Company'] if 'Company' in validation_df.columns else row.iloc[-1]}"
        )

        elements.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

else:

    elements.append(
        Paragraph(
            "No Validation Issues Found",
            styles["BodyText"]
        )
    )

elements.append(PageBreak())

# ---------------------------------
# TOP RECOMMENDATIONS
# ---------------------------------

elements.append(
    Paragraph(
        "Top Investment Recommendations",
        styles["Heading1"]
    )
)

elements.append(Spacer(1, 10))

if not rec_df.empty:

    for _, row in rec_df.head(20).iterrows():

        company = row["company_id"]

        roe = round(
            float(row["avg_roe"]),
            2
        )

        npm = round(
            float(row["avg_npm"]),
            2
        )

        score = round(
            float(row["score"]),
            2
        )

        text = f"""
        Company : {company}<br/>
        Average ROE : {roe}<br/>
        Average Net Profit Margin : {npm}<br/>
        Overall Score : {score}
        """

        elements.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 8)
        )

else:

    elements.append(
        Paragraph(
            "Recommendation File Not Found",
            styles["BodyText"]
        )
    )

elements.append(PageBreak())

# ---------------------------------
# PROJECT SUMMARY
# ---------------------------------

elements.append(
    Paragraph(
        "Project Summary",
        styles["Heading1"]
    )
)

elements.append(
    Paragraph(
        """
        The N100 Financial Intelligence Platform
        successfully integrates company data,
        financial ratios, stock prices, sector
        information and recommendation analytics
        into a unified SQLite database and
        Streamlit dashboard.
        """,
        styles["BodyText"]
    )
)

elements.append(Spacer(1, 10))

elements.append(
    Paragraph(
        "Sprint 1 Status : COMPLETED",
        styles["Heading2"]
    )
)

# ---------------------------------
# BUILD PDF
# ---------------------------------

pdf.build(elements)

print("=" * 50)
print("PDF REPORT CREATED SUCCESSFULLY")
print("Location: reports/company_report.pdf")
print("=" * 50)