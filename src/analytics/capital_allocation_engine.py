import sqlite3
import pandas as pd
import os

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT
    company_id,
    year,
    operating_activity,
    investing_activity,
    financing_activity
FROM cashflow
""", conn)

conn.close()


def sign(value):
    if pd.isna(value):
        return "0"
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "0"


def classify(cfo, cfi, cff):

    if cfo == "+" and cfi == "-" and cff == "-":
        return "Reinvestment"

    if cfo == "+" and cfi == "-" and cff == "+":
        return "Growth Funded by Debt"

    if cfo == "+" and cfi == "+" and cff == "-":
        return "Shareholder Returns"

    if cfo == "+" and cfi == "+" and cff == "+":
        return "Cash Accumulator"

    if cfo == "-" and cfi == "-" and cff == "+":
        return "Distress Signal"

    if cfo == "-" and cfi == "-" and cff == "-":
        return "Pre-Revenue"

    return "Mixed"


df["cfo_sign"] = df["operating_activity"].apply(sign)
df["cfi_sign"] = df["investing_activity"].apply(sign)
df["cff_sign"] = df["financing_activity"].apply(sign)

df["pattern"] = df.apply(
    lambda x: classify(
        x["cfo_sign"],
        x["cfi_sign"],
        x["cff_sign"]
    ),
    axis=1
)

os.makedirs("output", exist_ok=True)

df.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("=" * 60)
print("CAPITAL ALLOCATION ENGINE")
print("=" * 60)
print()
print(df.head(20))
print()
print("Rows :", len(df))
print()
print("Saved : output/capital_allocation.csv")