from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/valuation",
    tags=["Valuation"]
)

@router.get("/{company_id}")
def get_valuation(company_id: str):
    conn = get_connection()

    df = pd.read_sql("""
        SELECT
            company_id,
            year,
            face_value,
            book_value,
            roe_percentage,
            roce_percentage
        FROM financial_ratios fr
        JOIN companies c
        ON fr.company_id = c.id
        WHERE fr.company_id = ?
        ORDER BY year DESC
    """, conn, params=[company_id])

    conn.close()

    if df.empty:
        return {"error": "Company not found"}

    return {
        "rows": len(df),
        "data": df.fillna("").to_dict(orient="records")
    }