"""
N100 Financial Intelligence Platform
Sprint 2
Recommendation Engine
"""

import sqlite3
import pandas as pd
import numpy as np

DB = "data/nifty100.db"


class RecommendationEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        self.df = pd.read_sql(
            "SELECT * FROM company_rankings",
            self.conn
        )

        print("=" * 60)
        print("Recommendation Engine")
        print("=" * 60)

        print("Rows Loaded :", len(self.df))

    # -------------------------------------------------

    def generate_recommendations(self):

        print("\nGenerating Recommendations...")

        # Recommendation
        self.df["recommendation"] = np.select(
            [
                self.df["overall_score"] >= 35,
                self.df["overall_score"] >= 25
            ],
            [
                "BUY",
                "HOLD"
            ],
            default="SELL"
        )

        # Confidence Score (0–100)
        max_score = self.df["overall_score"].max()

        self.df["confidence_score"] = (
            self.df["overall_score"] / max_score * 100
        ).round(2)

        print("✓ Recommendations Generated")

        print("\nPreview\n")

        print(
            self.df[
                [
                    "company_id",
                    "year",
                    "overall_score",
                    "recommendation",
                    "confidence_score"
                ]
            ].head()
        )

    # -------------------------------------------------

    def save(self):

        recommendations = self.df[
            [
                "company_id",
                "year",
                "overall_score",
                "recommendation",
                "confidence_score"
            ]
        ]

        recommendations.to_sql(
            "company_recommendations",
            self.conn,
            if_exists="replace",
            index=False
        )

        print("\n✓ company_recommendations table created")
        print("Rows Saved :", len(recommendations))

    # -------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    engine = RecommendationEngine()

    engine.generate_recommendations()

    engine.save()

    engine.close()