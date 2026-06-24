import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql("""
SELECT
    company_id,
    return_on_equity_pct,
    net_profit_margin_pct,
    operating_profit_margin_pct,
    debt_to_equity
FROM financial_ratios
""", conn)

df = df.fillna(0)

df["Health_Score"] = (
    df["return_on_equity_pct"] * 0.30 +
    df["net_profit_margin_pct"] * 0.25 +
    df["operating_profit_margin_pct"] * 0.25 +
    (10 - df["debt_to_equity"]) * 0.20
)

health = df.groupby("company_id")["Health_Score"].mean().reset_index()

health = health.sort_values(
    "Health_Score",
    ascending=False
)

health.to_csv(
    "output/company_health_scores.csv",
    index=False
)

print(health.head(10))

conn.close()