"""
N100 Financial Intelligence Platform
Sprint 5
Sector Report Generator
"""

import sqlite3
import pandas as pd
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

DB = "data/nifty100.db"

OUTPUT = Path("reports/sector")
OUTPUT.mkdir(parents=True, exist_ok=True)


class SectorReport:

    def __init__(self):

        print("=" * 60)
        print("Sector Report Generator")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.sectors = pd.read_sql(
            """
            SELECT *
            FROM sectors
            """,
            self.conn
        )

        self.ratios = pd.read_sql(
            """
            SELECT company_id,
                   year,
                   return_on_equity_pct,
                   roce_pct,
                   net_profit_margin_pct
            FROM financial_ratios
            """,
            self.conn
        )

        print("Sector Rows :", len(self.sectors))
        print("Ratio Rows  :", len(self.ratios))

    # --------------------------------------------------

    def generate(self):

        styles = getSampleStyleSheet()

        merged = pd.merge(
            self.sectors,
            self.ratios,
            on="company_id",
            how="left"
        )

        merged = merged.sort_values("year")

        latest = merged.groupby("company_id").tail(1)

        generated = 0

        for sector in sorted(latest["broad_sector"].dropna().unique()):

            data = latest[
                latest["broad_sector"] == sector
            ]

            pdf_file = str(
                OUTPUT / f"{sector}_report.pdf"
            )

            doc = SimpleDocTemplate(pdf_file)

            story = []

            story.append(
                Paragraph(
                    f"<b>{sector} Sector Report</b>",
                    styles["Title"]
                )
            )

            story.append(Spacer(1, 15))

            summary = [
                ["Metric", "Value"],
                ["Companies", str(len(data))],
                ["Average ROE", f"{data['return_on_equity_pct'].mean():.2f}"],
                ["Average ROCE", f"{data['roce_pct'].mean():.2f}"],
                ["Average Margin", f"{data['net_profit_margin_pct'].mean():.2f}"],
            ]

            table = Table(summary)

            table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
                    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                    ("GRID", (0,0), (-1,-1), 1, colors.black),
                    ("BACKGROUND", (0,1), (-1,-1), colors.beige),
                ])
            )

            story.append(table)

            story.append(Spacer(1,20))

            company_table = [["Company"]]

            for company in sorted(data["company_id"].unique()):
                company_table.append([company])

            company_list = Table(company_table)

            company_list.setStyle(
                TableStyle([
                    ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                    ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),
                ])
            )

            story.append(company_list)

            doc.build(story)

            generated += 1

        print()
        print("Sector PDFs :", generated)

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = SectorReport()

    app.load_data()

    app.generate()

    app.close()