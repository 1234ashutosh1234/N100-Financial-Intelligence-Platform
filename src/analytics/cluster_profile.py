"""
N100 Financial Intelligence Platform
Sprint 6
Cluster Profiling
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB = "data/nifty100.db"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


class ClusterProfiler:

    def __init__(self):

        print("=" * 60)
        print("Cluster Profiling")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.cluster = pd.read_csv(
            OUTPUT / "cluster_labels.csv"
        )

        self.ratios = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                return_on_equity_pct,
                debt_to_equity,
                sales_cagr_pct,
                free_cash_flow_cr,
                operating_profit_margin_pct
            FROM financial_ratios
            """,
            self.conn
        )

    # --------------------------------------------------

    def generate(self):

        latest = (
            self.ratios
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )

        df = pd.merge(
            latest,
            self.cluster,
            on="company_id"
        )

        profile = (

            df.groupby("cluster_name")[

                [

                    "return_on_equity_pct",

                    "debt_to_equity",

                    "sales_cagr_pct",

                    "free_cash_flow_cr",

                    "operating_profit_margin_pct"

                ]

            ]

            .mean()

            .round(2)

        )

        profile.to_csv(

            OUTPUT / "cluster_profile.csv"

        )

        print()

        print("✓ cluster_profile.csv created")

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = ClusterProfiler()

    app.load_data()

    app.generate()

    app.close()