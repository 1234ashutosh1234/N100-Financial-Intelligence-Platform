"""
N100 Financial Intelligence Platform
Sprint 3
Peer Percentile Ranking Engine
"""

import sqlite3
import pandas as pd

DB = "data/nifty100.db"


class PeerRankingEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        print("=" * 60)
        print("Peer Ranking Engine")
        print("=" * 60)

        self.load_data()

    # --------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql("""
            SELECT *
            FROM financial_ratios
        """, self.conn)

        print("Rows :", len(self.df))

    # --------------------------------------------------

    def calculate_percentiles(self):

        print("\nCalculating Percentile Rankings...")

        metrics = [

            "return_on_equity_pct",

            "roce_pct",

            "net_profit_margin_pct",

            "debt_to_equity",

            "free_cash_flow_cr",

            "sales_cagr_pct",

            "profit_cagr_pct",

            "eps_cagr_pct"

        ]

        result = self.df[
            [
                "company_id",
                "year"
            ]
        ].copy()

        for metric in metrics:

            ascending = False

            if metric == "debt_to_equity":
                ascending = True

            result[metric + "_rank"] = (
                self.df[metric]
                .rank(
                    pct=True,
                    ascending=ascending
                ) * 100
            ).round(2)

        self.peer_df = result

        print("✓ Percentiles Calculated")

        print(self.peer_df.head())

    # --------------------------------------------------

    def save(self):

        self.peer_df.to_sql(

            "peer_percentiles",

            self.conn,

            if_exists="replace",

            index=False

        )

        print("\n✓ SQLite table saved")

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


# --------------------------------------------------

if __name__ == "__main__":

    engine = PeerRankingEngine()

    engine.calculate_percentiles()

    engine.save()

    engine.close()