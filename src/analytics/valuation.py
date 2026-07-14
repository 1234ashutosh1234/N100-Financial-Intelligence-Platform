"""
N100 Financial Intelligence Platform
Sprint 4
Valuation Engine
"""

import sqlite3
import pandas as pd

DB = "data/nifty100.db"


class ValuationEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        print("=" * 60)
        print("Valuation Engine")
        print("=" * 60)

        self.load_data()

    # ----------------------------------------

    def load_data(self):

        self.market = pd.read_sql(
            "SELECT * FROM market_cap",
            self.conn
        )

        print("Rows :", len(self.market))

    # ----------------------------------------

    def calculate(self):

        print("\nCalculating Valuation...")

        df = self.market.copy()

        df["valuation_flag"] = "Fair"

        df.loc[
            df["pe_ratio"] < 15,
            "valuation_flag"
        ] = "Undervalued"

        df.loc[
            df["pe_ratio"] > 30,
            "valuation_flag"
        ] = "Overvalued"

        df["value_score"] = (
            (
                30 - df["pe_ratio"].fillna(30)
            ).clip(lower=0)
            +
            (
                5 - df["pb_ratio"].fillna(5)
            ).clip(lower=0)
        ).round(2)

        self.df = df

        print("✓ Valuation Completed")

    # ----------------------------------------

    def save(self):

        self.df.to_sql(
            "valuation_summary",
            self.conn,
            if_exists="replace",
            index=False
        )

        self.df.to_excel(
            "output/valuation_summary.xlsx",
            index=False
        )

        self.df[
            [
                "company_id",
                "year",
                "valuation_flag",
                "value_score"
            ]
        ].to_csv(
            "output/valuation_flags.csv",
            index=False
        )

        print("✓ valuation_summary table saved")
        print("✓ valuation_summary.xlsx created")
        print("✓ valuation_flags.csv created")

    # ----------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    engine = ValuationEngine()

    engine.calculate()

    engine.save()

    engine.close()