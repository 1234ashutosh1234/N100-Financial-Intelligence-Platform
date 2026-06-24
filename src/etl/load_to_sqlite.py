import pandas as pd
import sqlite3

DB_PATH = "data/nifty100.db"

FILES = {
    "companies": "data/raw/companies.xlsx",
    "profitandloss": "data/raw/profitandloss.xlsx",
    "balancesheet": "data/raw/balancesheet.xlsx",
    "cashflow": "data/raw/cashflow.xlsx",
    "analysis": "data/raw/analysis.xlsx",
    "documents": "data/raw/documents.xlsx",
    "prosandcons": "data/raw/prosandcons.xlsx",
    "sectors": "data/raw/sectors.xlsx",
    "market_cap": "data/raw/market_cap.xlsx",
    "financial_ratios": "data/raw/financial_ratios.xlsx",
    "stock_prices": "data/raw/stock_prices.xlsx",
    "peer_groups": "data/raw/peer_groups.xlsx"
}

conn = sqlite3.connect(DB_PATH)

for table_name, file_path in FILES.items():
    print(f"Loading {table_name}...")

    df = pd.read_excel(file_path, engine="openpyxl")

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {table_name}: {len(df)} rows")

conn.close()

print("Database Created Successfully!")