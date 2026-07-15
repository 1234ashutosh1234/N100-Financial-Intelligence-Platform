"""
N100 Financial Intelligence Platform
Sprint 5
Cash Flow Intelligence Engine
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB = "data/nifty100.db"
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


class CashFlowIntelligence:

    def __init__(self):

        print("=" * 60)
        print("Cash Flow Intelligence Engine")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.cashflow = pd.read_sql(
            """
            SELECT *
            FROM cashflow
            """,
            self.conn
        )

        print("Cashflow Rows :", len(self.cashflow))

    # --------------------------------------------------

    def calculate(self):

        df = self.cashflow.copy()

        numeric_cols = [
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        records = []

        for company, group in df.groupby("company_id"):

            latest = (
                group.sort_values("year")
                .iloc[-1]
            )

            cfo = latest["operating_activity"]
            cfi = latest["investing_activity"]
            cff = latest["financing_activity"]
            net = latest["net_cash_flow"]

            # ----------------------------------
            # CFO Quality
            # ----------------------------------

            if cfo > 0:
                cfo_quality = "High"

            elif cfo > -100:
                cfo_quality = "Moderate"

            else:
                cfo_quality = "Poor"

            # ----------------------------------
            # Capex Label
            # ----------------------------------

            if cfi < -1000:
                capex_label = "Capital Intensive"

            elif cfi < 0:
                capex_label = "Moderate"

            else:
                capex_label = "Asset Light"

            # ----------------------------------
            # Distress
            # ----------------------------------

            distress_flag = (
                "Yes"
                if (cfo < 0 and cff > 0)
                else "No"
            )

            # ----------------------------------
            # Deleveraging
            # ----------------------------------

            deleveraging_flag = (
                "Yes"
                if cff < 0
                else "No"
            )

            records.append({

                "company_id": company,

                "year": latest["year"],

                "operating_activity": cfo,

                "investing_activity": cfi,

                "financing_activity": cff,

                "net_cash_flow": net,

                "cfo_quality": cfo_quality,

                "capex_label": capex_label,

                "distress_flag": distress_flag,

                "deleveraging_flag": deleveraging_flag

            })

        self.output = pd.DataFrame(records)

    # --------------------------------------------------

    def save(self):

        excel_file = OUTPUT / "cashflow_intelligence.xlsx"
        distress_file = OUTPUT / "distress_alerts.csv"

        self.output.to_excel(
            excel_file,
            index=False
        )

        self.output[
            self.output["distress_flag"] == "Yes"
        ].to_csv(
            distress_file,
            index=False
        )

        print()
        print("✓ Saved :", excel_file)

        print("✓ Saved :", distress_file)

        print()

        print("Companies :", len(self.output))

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    app = CashFlowIntelligence()

    app.load_data()

    app.calculate()

    app.save()

    app.close()