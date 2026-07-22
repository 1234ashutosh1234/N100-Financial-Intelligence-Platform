"""
N100 Financial Intelligence Platform
Sprint 6
Outlier Detection
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB = "data/nifty100.db"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


class OutlierDetection:

    def __init__(self):

        print("=" * 60)
        print("Outlier Detection")
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

    def generate(self):

        latest = (
            self.df
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
            .reset_index(drop=True)
        )

        metrics = [
            "return_on_equity_pct",
            "debt_to_equity",
            "sales_cagr_pct",
            "profit_cagr_pct",
            "eps_cagr_pct",
            "free_cash_flow_cr",
            "operating_profit_margin_pct",
            "net_profit_margin_pct",
            "roce_pct"
        ]

        records = []

        for metric in metrics:

            values = pd.to_numeric(
                latest[metric],
                errors="coerce"
            )

            mean = values.mean()
            std = values.std()

            if std == 0 or pd.isna(std):
                continue

            z = (values - mean) / std

            flagged = latest[abs(z) > 3]

            for _, row in flagged.iterrows():

                records.append({

                    "company_id": row["company_id"],

                    "metric": metric,

                    "value": row[metric],

                    "z_score": round(
                        float(z.loc[row.name]),
                        2
                    )

                })

        report = pd.DataFrame(records)

        report.to_csv(
            OUTPUT / "outlier_report.csv",
            index=False
        )

        print()

        print("✓ outlier_report.csv created")

        print("Outliers Found :", len(report))

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = OutlierDetection()

    app.load_data()

    app.generate()

    app.close()