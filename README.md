# 📈 N100 Financial Intelligence Platform

A comprehensive financial intelligence platform for NIFTY 100 companies built using **FastAPI**, **SQLite**, **Pandas**, **Streamlit**, and **Plotly**.

---

## 🚀 Features

### ✅ Company Information
- Company Details
- NSE & BSE Links
- Company Profiles
- Financial Overview

### 📊 Financial Analysis
- Historical Financial Ratios
- ROE Analysis
- ROCE Analysis
- Profit Margin
- Growth Score
- Financial Health Score

### 💰 Valuation
- Book Value
- Face Value
- ROE
- ROCE
- Valuation Metrics

### 🔍 Stock Screener
- Filter by ROE
- Filter by ROCE
- Filter by Growth Score
- Dynamic Query Parameters

Example:

```
/screener?min_roe=20&min_roce=25&min_growth=2
```

### 🏢 Sector Analysis
- Companies by Sector
- Average Index Weight
- Sector Distribution

### 🤖 Recommendation Engine
Automatic BUY / HOLD / SELL recommendation based on:

- ROE
- ROCE
- Profit Margin
- Growth Score

### ⚠ Risk Analysis
Evaluates company risk using:

- Debt to Equity
- Interest Coverage
- ROE
- Profit Margin

Risk Levels:
- Low Risk
- Medium Risk
- High Risk

### 👥 Peer Comparison
Compare a company with its sector peers using:

- ROE
- ROCE
- Sector Ranking

---

# 🛠 Tech Stack

- Python 3.14
- FastAPI
- SQLite
- Pandas
- Streamlit
- Plotly
- Uvicorn

---

# 📂 Project Structure

```
N100-Financial-Intelligence-Platform
│
├── data/
│   └── nifty100.db
│
├── src/
│   ├── analytics/
│   └── api/
│       ├── routers/
│       │   ├── health.py
│       │   ├── companies.py
│       │   ├── financials.py
│       │   ├── valuation.py
│       │   ├── screener.py
│       │   ├── sectors.py
│       │   ├── recommendation.py
│       │   ├── risk.py
│       │   └── peer.py
│       │
│       ├── database.py
│       └── main.py
│
├── dashboard/
└── README.md
```

---

# 🌐 Available APIs

| Endpoint | Description |
|----------|-------------|
| `/health` | Health Check |
| `/companies` | List Companies |
| `/companies/{id}` | Company Details |
| `/financials/{id}` | Financial Ratios |
| `/valuation/{id}` | Valuation Metrics |
| `/portfolio/stats` | Portfolio Statistics |
| `/screener` | Stock Screener |
| `/sectors` | Sector Analysis |
| `/recommendation/{id}` | BUY/HOLD/SELL Recommendation |
| `/risk/{id}` | Risk Analysis |
| `/peer/{id}` | Peer Comparison |

---

# ▶ Running the API

Activate the virtual environment:

```
venv\Scripts\activate
```

Run FastAPI:

```
python -m uvicorn src.api.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 📅 Sprint Status

## ✅ Sprint 6 Completed

Completed APIs:

- Health API
- Companies API
- Financials API
- Portfolio API
- Valuation API
- Screener API
- Sector Analysis API
- Recommendation API
- Risk Analysis API
- Peer Comparison API

---

## 🚀 Next Sprint

Sprint 7

- Streamlit Dashboard
- Interactive Charts
- Portfolio Dashboard
- Company Analysis UI
- AI Recommendation Dashboard
- Peer Comparison Charts