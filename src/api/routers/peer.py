from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/peer",
    tags=["Peer Comparison"]
)

@router.get("/{company_id}")
def peer_comparison(company_id: str):

    conn = get_connection()

    # Find the sector of the selected company
    company = pd.read_sql("""
        SELECT broad_sector
        FROM sectors
        WHERE company_id = ?
        LIMIT 1
    """, conn, params=[company_id])

    if company.empty:
        conn.close()
        return {"error": "Company not found"}

    sector = company.iloc[0]["broad_sector"]

    # Get peers in the same sector
    peers = pd.read_sql("""
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            c.roe_percentage,
            c.roce_percentage
        FROM companies c
        JOIN sectors s
            ON c.id = s.company_id
        WHERE s.broad_sector = ?
        ORDER BY c.roe_percentage DESC
        LIMIT 10
    """, conn, params=[sector])

    conn.close()

    return {
        "company": company_id,
        "sector": sector,
        "count": len(peers),
        "peers": peers.fillna("").to_dict(orient="records")
    }