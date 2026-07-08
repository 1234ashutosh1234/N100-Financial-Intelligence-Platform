"""
N100 Financial Intelligence Platform
Sprint 3
Peer Comparison Report
"""

import sqlite3
import pandas as pd

DB = "data/nifty100.db"


class PeerComparisonEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        print("=" * 60)
        print("Peer Comparison Report")
        print("=" * 60)

        self.load_data()

    # --------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT *
            FROM peer_percentiles
            """,
            self.conn
        )

        print("Rows Loaded :", len(self.df))

    # --------------------------------------------------

    def create_report(self):

        print("\nGenerating Excel Report...")

        metrics = [

            "return_on_equity_pct_rank",
            "roce_pct_rank",
            "net_profit_margin_pct_rank",
            "debt_to_equity_rank",
            "free_cash_flow_cr_rank",
            "sales_cagr_pct_rank",
            "profit_cagr_pct_rank",
            "eps_cagr_pct_rank"

        ]

        output = "output/peer_comparison.xlsx"

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            summary = self.df.copy()

            summary.to_excel(
                writer,
                sheet_name="All Companies",
                index=False
            )

            for metric in metrics:

                rank_df = self.df[
                    [
                        "company_id",
                        "year",
                        metric
                    ]
                ].sort_values(
                    by=metric,
                    ascending=False
                )

                sheet = metric.replace("_rank", "")

                sheet = sheet[:31]

                rank_df.to_excel(
                    writer,
                    sheet_name=sheet,
                    index=False
                )

        print("✓ peer_comparison.xlsx created")

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    engine = PeerComparisonEngine()

    engine.create_report()

    engine.close()