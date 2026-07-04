import sqlite3
import pandas as pd

DB = "data/nifty100.db"

FILES = {
    "companies": "data/raw/companies.xlsx",
    "analysis": "data/raw/analysis.xlsx",
    "documents": "data/raw/documents.xlsx",
    "prosandcons": "data/raw/prosandcons.xlsx"
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

        while "__" in c:
            c = c.replace("__", "_")

        cols.append(c.lower())

    df.columns = cols

    return df


conn = sqlite3.connect(DB)

for table, file in FILES.items():

    print("=" * 60)
    print("Repairing :", table)

    # These files use the second row as the header
    df = pd.read_excel(file, header=1)

    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")

    df = clean_columns(df)

    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False
    )

    print("Rows :", len(df))
    print("Columns :", len(df.columns))
    print(df.columns.tolist())

conn.close()

print("\nMetadata tables repaired successfully.")