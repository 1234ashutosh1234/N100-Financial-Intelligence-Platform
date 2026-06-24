import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        return_on_equity_pct
    FROM financial_ratios
    """,
    conn
)

print(sectors.head())

sectors.to_csv(
    "output/sector_analysis.csv",
    index=False
)

conn.close()