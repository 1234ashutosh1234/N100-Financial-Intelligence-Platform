import pandas as pd
from src.api.database import get_connection

conn = get_connection()

try:
    df = pd.read_sql("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """, conn)

    print("SUCCESS")
    print(df.head())
    print(df.columns.tolist())
    print("Rows:", len(df))

except Exception as e:
    print("ERROR:", e)

finally:
    conn.close()