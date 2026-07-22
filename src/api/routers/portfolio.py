from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

@router.get("/stats")
def portfolio_stats():
    conn = get_connection()

    df = pd.read_sql("""
        SELECT *
        FROM financial_ratios
    """, conn)

    conn.close()

    df = df.fillna(0)

    stats = {
        "companies": int(df["company_id"].nunique()),
        "records": int(len(df)),
        "avg_roe": round(df["return_on_equity_pct"].mean(), 2),
        "avg_roce": round(df["roce_pct"].mean(), 2),
        "avg_profit_margin": round(df["net_profit_margin_pct"].mean(), 2),
        "avg_growth_score": round(df["growth_score"].mean(), 2),
        "max_roe": round(df["return_on_equity_pct"].max(), 2),
        "min_roe": round(df["return_on_equity_pct"].min(), 2)
    }

    return stats