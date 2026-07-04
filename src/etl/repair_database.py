import sqlite3
import pandas as pd

DB = "data/nifty100.db"

FILES = {
    "profitandloss": "data/raw/profitandloss.xlsx",
    "balancesheet": "data/raw/balancesheet.xlsx",
    "cashflow": "data/raw/cashflow.xlsx",
}


def clean_columns(df):
    cols = []

    for c in df.columns:
        c = str(c).strip()
        c = c.replace("%", "_pct")
        c = c.replace("/", "_")
        c = c.replace("-", "_")
        c = c.replace("(", "")
        c = c.replace(")", "")
        c = c.replace(" ", "_")
        c = c.replace("__", "_")
        cols.append(c.lower())

    df.columns = cols
    return df


conn = sqlite3.connect(DB)

for table, file in FILES.items():

    print(f"\nLoading {table}...")

    # Header starts from second row
    df = pd.read_excel(file, header=1)

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Clean column names
    df = clean_columns(df)

    # Save back to SQLite
    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"{table} repaired successfully.")
    print(df.columns.tolist())

conn.close()

print("\nDatabase Repair Completed Successfully!")