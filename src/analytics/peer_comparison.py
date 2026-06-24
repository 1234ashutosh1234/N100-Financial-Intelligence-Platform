import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

query = """
SELECT
    company_id,
    return_on_equity_pct,
    net_profit_margin_pct,
    debt_to_equity
FROM financial_ratios
"""

df = pd.read_sql(query, conn)

peer = df.groupby("company_id").agg({
    "return_on_equity_pct":"mean",
    "net_profit_margin_pct":"mean",
    "debt_to_equity":"mean"
}).reset_index()

peer = peer.sort_values(
    "return_on_equity_pct",
    ascending=False
)

peer.to_csv(
    "output/peer_comparison.csv",
    index=False
)

print(peer.head(10))

conn.close()