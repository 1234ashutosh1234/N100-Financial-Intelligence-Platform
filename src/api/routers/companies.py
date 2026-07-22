from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import math
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

    records = []

    for row in df.to_dict(orient="records"):
        cleaned = {}
        for k, v in row.items():
            if isinstance(v, float) and math.isnan(v):
                cleaned[k] = None
            else:
                cleaned[k] = v
        records.append(cleaned)

    return JSONResponse(content=records)


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

    row = df.iloc[0].to_dict()

    cleaned = {}
    for k, v in row.items():
        if isinstance(v, float) and math.isnan(v):
            cleaned[k] = None
        else:
            cleaned[k] = v

    return JSONResponse(content=cleaned)