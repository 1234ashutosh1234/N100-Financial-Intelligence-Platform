import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql(
    "PRAGMA table_info(companies)",
    conn
)

print(df[["name"]])

conn.close()