import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql("""
SELECT
    company_id,
    AVG(return_on_equity_pct) as avg_roe,
    AVG(net_profit_margin_pct) as avg_margin,
    AVG(debt_to_equity) as avg_debt
FROM financial_ratios
GROUP BY company_id
""", conn)

df["Investment_Rating"] = df["avg_roe"].apply(
    lambda x: "Strong Buy" if x > 20 else
              "Buy" if x > 15 else
              "Hold"
)

df.to_csv(
    "output/company_scorecard.csv",
    index=False
)

print(df.head())

conn.close()