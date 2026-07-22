from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/risk",
    tags=["Risk Analysis"]
)


@router.get("/{company_id}")
def get_risk(company_id: str):

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
        return {"error": "Company not found"}

    row = df.iloc[0]

    score = 0
    risks = []

    # Debt
    if row["debt_to_equity"] > 1:
        score += 30
        risks.append("High Debt")

    # Interest Coverage
    if row["interest_coverage"] < 3:
        score += 30
        risks.append("Low Interest Coverage")

    # ROE
    if row["return_on_equity_pct"] < 10:
        score += 20
        risks.append("Weak ROE")

    # Profit Margin
    if row["net_profit_margin_pct"] < 10:
        score += 20
        risks.append("Low Profit Margin")

    if score <= 20:
        level = "Low Risk"
    elif score <= 50:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return {
        "company": company_id,
        "risk_score": score,
        "risk_level": level,
        "risk_factors": risks
    }