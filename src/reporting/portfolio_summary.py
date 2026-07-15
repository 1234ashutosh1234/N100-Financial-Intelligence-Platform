"""
N100 Financial Intelligence Platform
Sprint 5
Portfolio Summary Report
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

OUTPUT = Path("reports/portfolio")
OUTPUT.mkdir(parents=True, exist_ok=True)


class PortfolioSummary:

    def __init__(self):

        print("=" * 60)
        print("Portfolio Summary Generator")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.ranking = pd.read_sql(
            """
            SELECT *
            FROM company_rankings
            """,
            self.conn
        )

        self.sectors = pd.read_sql(
            """
            SELECT *
            FROM sectors
            """,
            self.conn
        )

        self.recommendation = pd.read_sql(
            """
            SELECT *
            FROM company_recommendations
            """,
            self.conn
        )

        print("Ranking Rows :", len(self.ranking))
        print("Sector Rows  :", len(self.sectors))
        print("Recommendation Rows :", len(self.recommendation))

    # --------------------------------------------------

    def generate(self):

        styles = getSampleStyleSheet()

        pdf_file = str(
            OUTPUT / "portfolio_summary.pdf"
        )

        doc = SimpleDocTemplate(pdf_file)

        story = []

        story.append(
            Paragraph(
                "<b>N100 Financial Intelligence Platform</b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 20))

        latest_rank = (
            self.ranking
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )

        latest_rec = (
            self.recommendation
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )

        summary = [

            ["Metric", "Value"],

            ["Companies",
             str(latest_rank["company_id"].nunique())],

            ["Average Overall Score",
             f"{latest_rank['overall_score'].mean():.2f}"],

            ["Average Rank",
             f"{latest_rank['overall_rank'].mean():.2f}"],

            ["Broad Sectors",
             str(self.sectors["broad_sector"].nunique())],

            ["Recommendations",
             str(latest_rec["recommendation"].nunique())]

        ]

        table = Table(summary)

        table.setStyle(
            TableStyle([
                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("GRID",(0,0),(-1,-1),1,colors.black),
                ("BACKGROUND",(0,1),(-1,-1),colors.beige),
            ])
        )

        story.append(table)

        story.append(Spacer(1, 25))

        story.append(
            Paragraph(
                "<b>Top 10 Companies</b>",
                styles["Heading2"]
            )
        )

        top10 = latest_rank.sort_values(
            "overall_rank"
        ).head(10)

        top_table = [["Company", "Overall Score", "Rank"]]

        for _, row in top10.iterrows():

            top_table.append([
                row["company_id"],
                round(row["overall_score"],2),
                int(row["overall_rank"])
            ])

        t = Table(top_table)

        t.setStyle(
            TableStyle([
                ("BACKGROUND",(0,0),(-1,0),colors.green),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("GRID",(0,0),(-1,-1),1,colors.black),
            ])
        )

        story.append(t)

        doc.build(story)

        print()

        print("✓ Portfolio Summary Created")

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = PortfolioSummary()

    app.load_data()

    app.generate()

    app.close()