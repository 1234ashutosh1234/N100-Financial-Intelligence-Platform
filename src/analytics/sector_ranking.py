import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

sector_df = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

sector_counts = sector_df.groupby(
    sector_df.columns[-1]
).size().reset_index(name="Companies")

sector_counts = sector_counts.sort_values(
    "Companies",
    ascending=False
)

sector_counts.to_csv(
    "output/sector_ranking.csv",
    index=False
)

print(sector_counts)

conn.close()