from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


@router.get("/{company_id}")
def get_recommendation(company_id: str):

    conn = get_connection()

    df = pd.read_sql("""
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
    """, conn, params=[company_id])

    conn.close()

    if df.empty:
        return {
            "error": "Company not found"
        }

    row = df.iloc[0]

    score = 0
    reasons = []

    # ROE
    if row["return_on_equity_pct"] >= 20:
        score += 25
        reasons.append("High ROE")

    # ROCE
    if row["roce_pct"] >= 20:
        score += 25
        reasons.append("High ROCE")

    # Profit Margin
    if row["net_profit_margin_pct"] >= 15:
        score += 20
        reasons.append("Healthy Profit Margin")

    # Growth
    if row["growth_score"] >= 2:
        score += 30
        reasons.append("Strong Growth")

    if score >= 80:
        recommendation = "BUY"
    elif score >= 50:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    return {
        "company": company_id,
        "score": score,
        "recommendation": recommendation,
        "reasons": reasons
    }