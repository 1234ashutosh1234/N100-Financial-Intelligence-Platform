"""
N100 Financial Intelligence Platform
Sprint 5
NLP Analysis Parser
"""

import sqlite3
import pandas as pd
import re
from pathlib import Path

DB = "data/nifty100.db"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


class AnalysisParser:

    def __init__(self):

        print("=" * 60)
        print("NLP Analysis Parser")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # -------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT *
            FROM analysis
            """,
            self.conn
        )

        print("Rows Loaded :", len(self.df))

    # -------------------------------------------------

    def parse_metrics(self):

        metric_columns = [
            "compounded_sales_growth",
            "compounded_profit_growth",
            "stock_price_cagr",
            "roe"
        ]

        pattern = r"(\d+)\s*Years?.*?(\d+\.?\d*)"

        parsed = []
        failed = []

        for _, row in self.df.iterrows():

            company = row["company_id"]

            for metric in metric_columns:

                text = str(row[metric])

                match = re.search(pattern, text)

                if match:

                    parsed.append({
                        "company_id": company,
                        "metric_type": metric,
                        "period_years": int(match.group(1)),
                        "value_pct": float(match.group(2))
                    })

                else:

                    failed.append({
                        "company_id": company,
                        "metric": metric,
                        "text": text
                    })

        self.parsed_df = pd.DataFrame(parsed)
        self.failed_df = pd.DataFrame(failed)

    # -------------------------------------------------

    def save_outputs(self):

        parsed_file = OUTPUT_DIR / "analysis_parsed.csv"
        failed_file = OUTPUT_DIR / "parsing_failures.csv"

        self.parsed_df.to_csv(parsed_file, index=False)
        self.failed_df.to_csv(failed_file, index=False)

        print()
        print("✓ Saved :", parsed_file)
        print("✓ Saved :", failed_file)

        print()
        print("Parsed Rows :", len(self.parsed_df))
        print("Failed Rows :", len(self.failed_df))

    # -------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    parser = AnalysisParser()

    parser.load_data()

    parser.parse_metrics()

    parser.save_outputs()

    parser.close()