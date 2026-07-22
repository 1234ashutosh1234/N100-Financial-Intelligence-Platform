"""
N100 Financial Intelligence Platform
Sprint 6
Correlation Heatmap
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DB = "data/nifty100.db"

REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)


class CorrelationHeatmap:

    def __init__(self):

        print("=" * 60)
        print("Correlation Heatmap")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT
                return_on_equity_pct,
                debt_to_equity,
                sales_cagr_pct,
                profit_cagr_pct,
                eps_cagr_pct,
                free_cash_flow_cr,
                operating_profit_margin_pct,
                net_profit_margin_pct,
                roce_pct,
                growth_score
            FROM financial_ratios
            """,
            self.conn
        )

    # --------------------------------------------------

    def generate(self):

        corr = self.df.corr(numeric_only=True)

        plt.figure(figsize=(10,8))

        plt.imshow(corr, cmap="coolwarm")

        plt.xticks(
            range(len(corr.columns)),
            corr.columns,
            rotation=90,
            fontsize=8
        )

        plt.yticks(
            range(len(corr.columns)),
            corr.columns,
            fontsize=8
        )

        plt.colorbar()

        plt.tight_layout()

        plt.savefig(
            REPORTS / "correlation_heatmap.png",
            dpi=200
        )

        plt.close()

        print("✓ correlation_heatmap.png created")

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = CorrelationHeatmap()

    app.load_data()

    app.generate()

    app.close()