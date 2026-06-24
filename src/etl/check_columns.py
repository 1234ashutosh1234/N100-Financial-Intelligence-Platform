import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

tables = [
    "companies",
    "financial_ratios",
    "sectors"
]

for table in tables:

    print(f"\n{table.upper()}")

    df = pd.read_sql(
        f"PRAGMA table_info({table})",
        conn
    )

    print(df[["name"]])

conn.close()