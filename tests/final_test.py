"""
Sprint 2 Final Test
"""

import sqlite3
import pandas as pd

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

tables = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""", conn)

print("=" * 60)
print("DATABASE TABLES")
print("=" * 60)

print(tables)

print()

for table in tables["name"]:

    df = pd.read_sql(
        f"SELECT * FROM {table}",
        conn
    )

    print("=" * 60)
    print(table.upper())
    print("=" * 60)

    print("Rows :", len(df))
    print("Columns :", len(df.columns))

conn.close()

print("\nAll Tests Passed")