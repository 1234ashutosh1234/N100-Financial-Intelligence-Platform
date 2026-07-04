import sqlite3
import pandas as pd
import os

DB = "data/nifty100.db"

conn = sqlite3.connect(DB)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# -------------------------------
# Merge sector information
# -------------------------------

df = ratios.merge(
    sectors[
        [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]
    ],
    on="company_id",
    how="left"
)

issues = []

for _, row in df.iterrows():

    company = row["company_id"]

    year = row["year"]

    sector = row["broad_sector"]

    # -------------------------
    # Financial Sector
    # -------------------------

    if pd.notna(sector):

        if sector.lower() == "financials":

            issues.append(
                [
                    company,
                    year,
                    "Financial Sector",
                    "ROCE benchmark skipped"
                ]
            )

    # -------------------------
    # High Debt
    # -------------------------

    if pd.notna(row["debt_to_equity"]):

        if row["debt_to_equity"] > 5:

            issues.append(
                [
                    company,
                    year,
                    "High Debt",
                    "Debt/Equity > 5"
                ]
            )

    # -------------------------
    # Negative ROE
    # -------------------------

    if pd.notna(row["return_on_equity_pct"]):

        if row["return_on_equity_pct"] < 0:

            issues.append(
                [
                    company,
                    year,
                    "Negative ROE",
                    "ROE below zero"
                ]
            )

    # -------------------------
    # Zero Margin
    # -------------------------

    if pd.notna(row["net_profit_margin_pct"]):

        if row["net_profit_margin_pct"] == 0:

            issues.append(
                [
                    company,
                    year,
                    "Zero Margin",
                    "Net Profit Margin = 0"
                ]
            )

edge_df = pd.DataFrame(
    issues,
    columns=[
        "Company",
        "Year",
        "Issue",
        "Description"
    ]
)

os.makedirs("output", exist_ok=True)

edge_df.to_csv(
    "output/ratio_edge_cases.log",
    index=False
)

print("=" * 60)
print("EDGE CASE ENGINE")
print("=" * 60)

print()

print(edge_df.head(20))

print()

print("Total Edge Cases :", len(edge_df))

print()

print("Saved")

print("output/ratio_edge_cases.log")