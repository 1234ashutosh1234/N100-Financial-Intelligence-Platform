import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql("""
SELECT
company_id,
AVG(return_on_equity_pct) as avg_roe,
AVG(net_profit_margin_pct) as avg_npm
FROM financial_ratios
GROUP BY company_id
""", conn)

df["score"] = (
    df["avg_roe"] * 0.6 +
    df["avg_npm"] * 0.4
)

top = df.sort_values(
    "score",
    ascending=False
)

top.to_csv(
    "output/top_recommendations.csv",
    index=False
)

print("Recommendations Created")