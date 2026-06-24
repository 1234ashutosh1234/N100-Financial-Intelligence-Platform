import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "financial_ratios",
    "stock_prices",
    "peer_groups"
]

results = []

for table in tables:

    count = pd.read_sql(
        f"SELECT COUNT(*) AS total FROM {table}",
        conn
    )

    results.append([
        table,
        int(count.iloc[0]["total"])
    ])

audit_df = pd.DataFrame(
    results,
    columns=["table_name", "row_count"]
)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print(audit_df)

print("Load Audit Created Successfully")