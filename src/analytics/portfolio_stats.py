"""
N100 Financial Intelligence Platform
Sprint 6
Portfolio Statistics
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

DB = "data/nifty100.db"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


class PortfolioStatistics:

    def __init__(self):

        print("=" * 60)
        print("Portfolio Statistics")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                return_on_equity_pct,
                debt_to_equity,
                sales_cagr_pct,
                profit_cagr_pct,
                eps_cagr_pct,
                free_cash_flow_cr,
                operating_profit_margin_pct,
                net_profit_margin_pct,
                roce_pct
            FROM financial_ratios
            """,
            self.conn
        )

    # --------------------------------------------------

    def calculate(self):

        latest = (
            self.df
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
            .reset_index(drop=True)
        )

        metrics = [

            "return_on_equity_pct",

            "roce_pct",

            "net_profit_margin_pct",

            "operating_profit_margin_pct",

            "debt_to_equity",

            "sales_cagr_pct",

            "profit_cagr_pct",

            "eps_cagr_pct",

            "free_cash_flow_cr"

        ]

        records = []

        for metric in metrics:

            values = pd.to_numeric(
                latest[metric],
                errors="coerce"
            ).dropna()

            records.append({

                "metric": metric,

                "P10": round(np.percentile(values,10),2),

                "P25": round(np.percentile(values,25),2),

                "P50": round(np.percentile(values,50),2),

                "P75": round(np.percentile(values,75),2),

                "P90": round(np.percentile(values,90),2),

                "Mean": round(values.mean(),2),

                "Std": round(values.std(),2)

            })

        self.output = pd.DataFrame(records)

    # --------------------------------------------------

    def save(self):

        self.output.to_csv(

            OUTPUT / "portfolio_stats.csv",

            index=False

        )

        print()

        print("✓ portfolio_stats.csv created")

        print()

        print(self.output)

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = PortfolioStatistics()

    app.load_data()

    app.calculate()

    app.save()

    app.close()