# N100 Financial Intelligence Platform - Analyst Guide

## Overview
The N100 Financial Intelligence Platform provides financial analysis, stock screening, peer comparison, valuation, and investment recommendations using FastAPI and SQLite.

## Tech Stack
- Python
- FastAPI
- SQLite
- Pandas
- Plotly
- Streamlit

## Running the API

```bash
python -m uvicorn src.api.main:app --reload
```

## API Documentation

http://127.0.0.1:8000/docs

## Available Endpoints

- GET /companies
- GET /companies/{company_id}
- GET /financials/{company_id}
- GET /valuation/{company_id}
- GET /portfolio
- GET /recommendation/{company_id}
- GET /risk/{company_id}
- GET /peer/{company_id}
- GET /screener
- GET /sectors

## Output Files

- cluster_labels.csv
- company_health_scores.csv
- valuation_flags.csv
- stock_screener.csv

## Testing

pytest --html=reports/pytest_report.html --self-contained-html