from fastapi import APIRouter
import pandas as pd
from src.api.database import get_connection

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.get("/")
def get_companies():

    conn = get_connection()

    df = pd.read_sql("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """, conn)

    conn.close()

    return df.to_dict(orient="records")


@router.get("/{company_id}")
def get_company(company_id: str):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    if df.empty:
        return {"message": "Company not found"}

    return df.iloc[0].to_dict()