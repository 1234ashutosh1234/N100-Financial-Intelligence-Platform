import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql("""
SELECT
    company_id,
    year,
    COUNT(*) AS cnt
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1
""", conn)

if df.empty:
    print("✅ No duplicate company-year records found.")
else:
    print("❌ Duplicate company-year records found:")
    print(df)

conn.close()