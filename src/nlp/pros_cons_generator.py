"""
N100 Financial Intelligence Platform
Sprint 5
Auto Pros & Cons Generator
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB = "data/nifty100.db"
OUTPUT = Path("output/pros_cons_generated.csv")


class ProsConsGenerator:

    def __init__(self):

        print("=" * 60)
        print("Auto Pros & Cons Generator")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # -------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn
        )

        print("Rows Loaded :", len(self.df))

    # -------------------------------------------------

    def generate(self):

        results = []

        for _, row in self.df.iterrows():

            pros = []
            cons = []

            # ---------- PRO RULES ----------

            if row["return_on_equity_pct"] >= 20:
                pros.append("High ROE")

            if row["roce_pct"] >= 20:
                pros.append("Strong ROCE")

            if row["debt_to_equity"] <= 0.5:
                pros.append("Low Debt")

            if row["free_cash_flow_cr"] > 0:
                pros.append("Positive Free Cash Flow")

            if row["sales_cagr_pct"] >= 15:
                pros.append("Strong Revenue Growth")

            if row["profit_cagr_pct"] >= 15:
                pros.append("Strong Profit Growth")

            # ---------- CON RULES ----------

            if row["debt_to_equity"] > 2:
                cons.append("High Debt")

            if row["return_on_equity_pct"] < 10:
                cons.append("Low ROE")

            if row["roce_pct"] < 10:
                cons.append("Low ROCE")

            if row["free_cash_flow_cr"] < 0:
                cons.append("Negative Free Cash Flow")

            if row["sales_cagr_pct"] < 5:
                cons.append("Weak Revenue Growth")

            if row["profit_cagr_pct"] < 5:
                cons.append("Weak Profit Growth")

            confidence = min(100, len(pros) * 15 + len(cons) * 10)

            results.append({
                "company_id": row["company_id"],
                "year": row["year"],
                "pros": "; ".join(pros),
                "cons": "; ".join(cons),
                "confidence_score": confidence
            })

        self.result = pd.DataFrame(results)

    # -------------------------------------------------

    def save(self):

        self.result.to_csv(OUTPUT, index=False)

        print()
        print("✓ Saved :", OUTPUT)
        print("Rows :", len(self.result))

    # -------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = ProsConsGenerator()

    app.load_data()

    app.generate()

    app.save()

    app.close()