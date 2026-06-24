import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

query = """
SELECT *
FROM financial_ratios
"""

df = pd.read_sql(query, conn)

print(df.head())

df.to_csv(
    "output/financial_ratios_report.csv",
    index=False
)

print("Financial Ratio Report Generated")

conn.close()