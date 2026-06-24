import pandas as pd
import sqlite3

df = pd.read_excel("data/raw/companies.xlsx")

print("Original Shape:", df.shape)
print(df.head())

# Use first data row as column names
df.columns = df.iloc[0]

# Remove header row
df = df[1:]

# Reset index
df.reset_index(drop=True, inplace=True)

print("\nNew Columns:")
print(df.columns)

conn = sqlite3.connect("data/nifty100.db")

df.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Companies table fixed successfully")