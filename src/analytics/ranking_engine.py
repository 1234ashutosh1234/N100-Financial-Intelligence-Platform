"""
N100 Financial Intelligence Platform
Sprint 2
Ranking Engine
"""

import sqlite3
import pandas as pd

DB = "data/nifty100.db"


class RankingEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        print("Financial Ratios Loaded")
        print("Rows :", len(self.df))

    # -----------------------------------

    def calculate_rankings(self):

        print("\nCalculating Rankings...")

        # Growth Rank
        self.df["growth_rank"] = (
            self.df["growth_score"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # Health Rank
        self.df["health_rank"] = (
            self.df["financial_health_score"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # Profitability Rank
        self.df["profitability_rank"] = (
            self.df["return_on_equity_pct"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # Overall Score

        self.df["overall_score"] = (

            self.df["growth_score"] +

            self.df["financial_health_score"] +

            self.df["return_on_equity_pct"]

        )

        # Overall Rank

        self.df["overall_rank"] = (

            self.df["overall_score"]

            .rank(
                ascending=False,
                method="dense"
            )

            .astype(int)

        )

        print("✓ Rankings Calculated")

        print(
            self.df[
                [
                    "company_id",
                    "year",
                    "overall_score",
                    "overall_rank",
                    "growth_rank",
                    "health_rank",
                    "profitability_rank"
                ]
            ].head()
        )

    # -----------------------------------

    def save(self):

        rankings = self.df[
            [
                "company_id",
                "year",
                "overall_score",
                "overall_rank",
                "growth_rank",
                "health_rank",
                "profitability_rank"
            ]
        ]

        rankings.to_sql(

            "company_rankings",

            self.conn,

            if_exists="replace",

            index=False

        )

        print("\ncompany_rankings table created")

    # -----------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    engine = RankingEngine()

    engine.calculate_rankings()

    engine.save()

    engine.close()