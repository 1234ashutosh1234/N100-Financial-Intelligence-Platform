import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

issues = []

rules = [

("DQ01","ROE < 0",
"""
SELECT company_id
FROM financial_ratios
WHERE return_on_equity_pct < 0
"""),

("DQ02","Debt < 0",
"""
SELECT company_id
FROM financial_ratios
WHERE debt_to_equity < 0
"""),

("DQ03","NPM < 0",
"""
SELECT company_id
FROM financial_ratios
WHERE net_profit_margin_pct < 0
"""),

("DQ04","OPM < 0",
"""
SELECT company_id
FROM financial_ratios
WHERE operating_profit_margin_pct < 0
"""),

("DQ05","ROE > 100",
"""
SELECT company_id
FROM financial_ratios
WHERE return_on_equity_pct > 100
"""),

("DQ06","Debt > 50",
"""
SELECT company_id
FROM financial_ratios
WHERE debt_to_equity > 50
"""),

("DQ07","Missing Company",
"""
SELECT company_id
FROM financial_ratios
WHERE company_id IS NULL
"""),

("DQ08","Missing Year",
"""
SELECT company_id
FROM financial_ratios
WHERE year IS NULL
"""),

("DQ09","Missing Sector",
"""
SELECT company_id
FROM sectors
WHERE broad_sector IS NULL
"""),

("DQ10","Missing Sub Sector",
"""
SELECT company_id
FROM sectors
WHERE sub_sector IS NULL
"""),

("DQ11","Face Value <0",
"""
SELECT company_name
FROM companies
WHERE face_value < 0
"""),

("DQ12","Book Value <0",
"""
SELECT company_name
FROM companies
WHERE book_value < 0
"""),

("DQ13","ROCE <0",
"""
SELECT company_name
FROM companies
WHERE roce_percentage < 0
"""),

("DQ14","ROE <0",
"""
SELECT company_name
FROM companies
WHERE roe_percentage < 0
"""),

("DQ15","Duplicate Company",
"""
SELECT company_name
FROM companies
GROUP BY company_name
HAVING COUNT(*) > 1
"""),

("DQ16","Missing Website",
"""
SELECT company_name
FROM companies
WHERE website IS NULL
""")
]

for rule_id, rule_name, query in rules:

    try:

        df = pd.read_sql(query, conn)

        for _, row in df.iterrows():

            issues.append([
                rule_id,
                rule_name,
                row.iloc[0]
            ])

    except:
        pass

result = pd.DataFrame(
    issues,
    columns=[
        "Rule_ID",
        "Issue",
        "Entity"
    ]
)

result.to_csv(
    "output/validation_failures.csv",
    index=False
)

print(result.head())

print("16 DQ Rules Completed")