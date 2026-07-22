from fastapi import APIRouter
import pandas as pd
import traceback
from src.api.database import get_connection

router = APIRouter(
    prefix="/financials",
    tags=["Financials"]
)

@router.get("/{company_id}")
def get_financials(company_id: str):
    try:
        conn = get_connection()

        df = pd.read_sql("""
            SELECT *
            FROM financial_ratios
            WHERE company_id = ?
            ORDER BY year DESC
        """, conn, params=[company_id])

        conn.close()

        return df.fillna("").to_dict(orient="records")
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }