from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)

@router.get("/")
def screener(
    min_roe: float = 0,
    min_roce: float = 0,
    min_growth: int = 0,
):
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        c.website,
        c.nse_profile,
        c.bse_profile,
        c.face_value,
        c.book_value,
        c.roe_percentage,
        c.roce_percentage,
        fr.year,
        fr.return_on_equity_pct,
        fr.roce_pct,
        fr.growth_score
    FROM companies c
    JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE
        fr.return_on_equity_pct >= ?
        AND fr.roce_pct >= ?
        AND fr.growth_score >= ?
    ORDER BY fr.return_on_equity_pct DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=[min_roe, min_roce, min_growth]
    )

    conn.close()

    return {
        "count": len(df),
        "data": df.fillna("").to_dict(orient="records")
    }