"""
N100 Financial Intelligence Platform
Sprint 5
Capital Pattern Change Report
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB = "data/nifty100.db"
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


class CapitalPatternChanges:

    def __init__(self):

        print("=" * 60)
        print("Capital Pattern Change Report")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT *
            FROM company_recommendations
            """,
            self.conn
        )

        print("Rows Loaded :", len(self.df))

    # --------------------------------------------------

    def generate(self):

        # Sort company history
        self.df = self.df.sort_values(
            ["company_id", "year"]
        )

        records = []

        for company, group in self.df.groupby("company_id"):

            group = group.reset_index(drop=True)

            if len(group) < 2:
                continue

            previous = group.iloc[-2]
            latest = group.iloc[-1]

            old_pattern = previous["recommendation"]
            new_pattern = latest["recommendation"]

            if old_pattern != new_pattern:

                records.append({

                    "company_id": company,

                    "previous_year": previous["year"],

                    "current_year": latest["year"],

                    "previous_pattern": old_pattern,

                    "current_pattern": new_pattern

                })

        self.output = pd.DataFrame(records)

    # --------------------------------------------------

    def save(self):

        file = OUTPUT / "pattern_changes.csv"

        self.output.to_csv(
            file,
            index=False
        )

        print()

        print("✓ Saved :", file)

        print("Pattern Changes :", len(self.output))

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = CapitalPatternChanges()

    app.load_data()

    app.generate()

    app.save()

    app.close()