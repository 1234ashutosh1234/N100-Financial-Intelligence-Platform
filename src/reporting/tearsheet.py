"""
N100 Financial Intelligence Platform
Sprint 5
Company Tearsheet Generator
"""

import sqlite3
import pandas as pd
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

DB = "data/nifty100.db"

OUTPUT = Path("reports/tearsheets")
OUTPUT.mkdir(parents=True, exist_ok=True)


class TearsheetGenerator:

    def __init__(self):

        print("=" * 60)
        print("Company Tearsheet Generator")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.ratios = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn
        )

        self.rankings = pd.read_sql(
            """
            SELECT *
            FROM company_rankings
            """,
            self.conn
        )

        print("Ratios :", len(self.ratios))
        print("Rankings :", len(self.rankings))

    # --------------------------------------------------

    def generate(self):

        styles = getSampleStyleSheet()

        companies = self.ratios["company_id"].unique()

        generated = 0

        for company in companies:

            latest = (
                self.ratios[
                    self.ratios["company_id"] == company
                ]
                .sort_values("year")
                .iloc[-1]
            )

            pdf = OUTPUT / f"{company}_tearsheet.pdf"

            doc = SimpleDocTemplate(str(pdf))
            story = []

            story.append(
                Paragraph(
                    f"<b>{company} Company Tearsheet</b>",
                    styles["Title"]
                )
            )

            story.append(Spacer(1, 15))

            table = Table([
                ["Metric", "Value"],

                ["Year", str(latest["year"])],

                ["ROE", str(latest["return_on_equity_pct"])],

                ["ROCE", str(latest["roce_pct"])],

                ["Net Margin", str(latest["net_profit_margin_pct"])],

                ["Debt/Equity", str(latest["debt_to_equity"])],

                ["Sales CAGR", str(latest["sales_cagr_pct"])],

                ["Profit CAGR", str(latest["profit_cagr_pct"])],

                ["EPS CAGR", str(latest["eps_cagr_pct"])]
            ])

            table.setStyle(

                TableStyle([

                    ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                    ("GRID",(0,0),(-1,-1),1,colors.black),

                    ("BACKGROUND",(0,1),(-1,-1),colors.beige)

                ])

            )

            story.append(table)

            story.append(Spacer(1,20))

            story.append(

                Paragraph(

                    "Generated automatically by the N100 Financial Intelligence Platform.",

                    styles["Normal"]

                )

            )

            doc.build(story)

            generated += 1

        print()

        print("PDFs Generated :", generated)

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = TearsheetGenerator()

    app.load_data()

    app.generate()

    app.close()