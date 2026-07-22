from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"]
)


@router.get("/")
def get_sectors():

    conn = get_connection()

    df = pd.read_sql("""
        SELECT
            broad_sector,
            COUNT(company_id) AS company_count,
            AVG(index_weight_pct) AS avg_weight
        FROM sectors
        GROUP BY broad_sector
        ORDER BY company_count DESC
    """, conn)

    conn.close()

    return {
        "count": len(df),
        "data": df.fillna("").to_dict(orient="records")
    }


@router.get("/{sector_name}")
def sector_companies(sector_name: str):

    conn = get_connection()

    df = pd.read_sql("""
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            s.sub_sector,
            s.market_cap_category
        FROM companies c
        JOIN sectors s
        ON c.id=s.company_id
        WHERE s.broad_sector=?
    """, conn, params=[sector_name])

    conn.close()

    return {
        "count": len(df),
        "data": df.fillna("").to_dict(orient="records")
    }