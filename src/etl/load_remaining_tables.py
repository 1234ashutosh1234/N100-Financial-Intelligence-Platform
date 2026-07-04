import sqlite3
import pandas as pd
import os

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

# -----------------------------
# Files to Load
# -----------------------------

FILES = {
    "companies": "data/raw/companies.xlsx",
    "analysis": "data/raw/analysis.xlsx",
    "documents": "data/raw/documents.xlsx",
    "prosandcons": "data/raw/prosandcons.xlsx",
    "peer_groups": "data/raw/peer_groups.xlsx",
    "sectors": "data/raw/sectors.xlsx",
    "stock_prices": "data/raw/stock_prices.xlsx",
    "market_cap": "data/raw/market_cap.xlsx",
}

# -----------------------------
# Clean Column Names
# -----------------------------

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

        while "__" in c:
            c = c.replace("__", "_")

        cols.append(c.lower())

    df.columns = cols

    return df


# -----------------------------
# Load Excel Files
# -----------------------------

for table, file in FILES.items():

    print("=" * 60)
    print("Loading :", table)

    if not os.path.exists(file):

        print("Missing :", file)

        continue

    # Most of these files have headers on the first row
    df = pd.read_excel(file)

    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")

    df = clean_columns(df)

    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False,
    )

    print("Rows :", len(df))
    print("Columns :", len(df.columns))
    print("Done.")

conn.close()

print("\n")
print("=" * 60)
print("Remaining Tables Loaded Successfully!")
print("=" * 60)