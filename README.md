# 📈 N100 Financial Intelligence Platform

A comprehensive Financial Analytics Platform for the Nifty 100 companies that performs financial ratio analysis, company ranking, growth analytics, and investment recommendations using Python, SQLite, Pandas, and Streamlit.

---

# 🚀 Project Overview

The N100 Financial Intelligence Platform is designed to analyze the financial performance of India's top companies by integrating financial statements, market data, and analytical metrics into a single platform.

The platform provides:

- Financial Ratio Analysis
- Growth Analytics
- Company Ranking
- Investment Recommendation Engine
- Interactive Streamlit Dashboard

---

# 🏆 Sprint 1 (Completed)

## Data Engineering & Database Development

### Objectives

- Collect financial datasets
- Design SQLite database
- Load datasets into database
- Prepare analytics-ready tables

### Completed Modules

- ✅ SQLite Database Creation
- ✅ ETL Pipeline
- ✅ Data Cleaning
- ✅ Duplicate Removal
- ✅ Company Data Integration
- ✅ Market Cap Data Loading
- ✅ Financial Statement Import
- ✅ Analysis Table Integration
- ✅ Documents Integration
- ✅ Pros & Cons Integration

### Database Tables

- companies
- balancesheet
- profitandloss
- cashflow
- market_cap
- analysis
- documents
- prosandcons

---

# 📊 Sprint 2 (Completed)

## Financial Analytics Engine

Sprint 2 introduces advanced financial analytics and investment intelligence.

### Part 1

### Data Merge Engine

Implemented a unified analytics dataframe by merging:

- Profit & Loss
- Balance Sheet
- Cash Flow
- Market Cap
- Analysis

---

### Part 2

### Financial Ratio Engine

Calculated:

- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Debt to Equity
- Interest Coverage Ratio
- Asset Turnover Ratio
- Free Cash Flow

---

### Part 3

### Advanced Financial KPIs

Implemented:

- ROCE
- ROA
- Financial Health Score

---

### Part 4

### Database Integration

Generated SQLite table:

financial_ratios

---

### Part 5

### Growth Analytics Engine

Calculated:

- Revenue CAGR
- Profit CAGR
- EPS CAGR
- Growth Score

---

### Part 6

### Ranking Engine

Generated:

- Growth Rank
- Financial Health Rank
- Profitability Rank
- Overall Company Score
- Overall Rank

SQLite Table:

company_rankings

---

### Part 7

### Recommendation Engine

Generated:

- BUY
- HOLD
- SELL

Confidence Score

SQLite Table:

company_recommendations

---

### Part 8

### Dashboard Integration

Developed Streamlit Dashboard featuring:

- KPI Cards
- Company Analysis
- Financial Ratios
- Company Rankings
- Investment Recommendations

---

# 🗄 Database Tables

## Sprint 1

- companies
- balancesheet
- profitandloss
- cashflow
- market_cap
- analysis
- documents
- prosandcons

## Sprint 2

- financial_ratios
- company_rankings
- company_recommendations

---

# 💻 Tech Stack

## Programming Language

- Python 3.14

## Database

- SQLite

## Data Analysis

- Pandas
- NumPy

## Dashboard

- Streamlit

## Development Tools

- VS Code
- Git
- GitHub

---

# 📂 Project Structure

```
N100-Financial-Intelligence-Platform
│
├── data
│   ├── nifty100.db
│   ├── analysis.xlsx
│   ├── balancesheet.xlsx
│   ├── cashflow.xlsx
│   ├── companies.xlsx
│   ├── market_cap.xlsx
│   ├── profitandloss.xlsx
│   └── ...
│
├── src
│   ├── analytics
│   │   ├── ratio_engine.py
│   │   ├── ranking_engine.py
│   │   ├── recommendation_engine.py
│   │   ├── cagr.py
│   │   ├── ratios.py
│   │   └── ...
│   │
│   ├── dashboard
│   │   ├── app.py
│   │   └── pages
│   │
│   ├── etl
│   │
│   └── api
│
├── tests
│
├── requirements.txt
│
└── README.md
```

---

# ⚙ Installation

Clone Repository

```bash
git clone https://github.com/1234ashutosh1234/N100-Financial-Intelligence-Platform
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run Analytics

Financial Ratio Engine

```bash
python -m src.analytics.ratio_engine
```

Ranking Engine

```bash
python -m src.analytics.ranking_engine
```

Recommendation Engine

```bash
python -m src.analytics.recommendation_engine
```

---

# 📈 Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard URL

```
http://localhost:8501
```

---

# 🧪 Testing

Run Final Test

```bash
python tests/final_test.py
```

---

# 📊 Features

- Financial Ratio Analysis
- Growth Analytics
- Company Ranking
- Recommendation Engine
- SQLite Database
- Streamlit Dashboard
- Financial Health Score
- CAGR Analytics
- ROE
- ROCE
- ROA
- Free Cash Flow Analysis

---

# 🎯 Future Scope (Sprint 3)

- Sector Analytics
- Peer Comparison
- Stock Screener
- Valuation Engine
- AI-Based Insights
- Interactive Charts
- PDF Report Generation
- Portfolio Analysis

---

# 👨‍💻 Developer

**Ashutosh Raj**

B.Tech – Computer Science & Engineering

Bihar Engineering University, Patna

---

# ⭐ Project Status

**Sprint 1:** ✅ Completed

**Sprint 2:** ✅ Completed

**Sprint 3:** 🚧 In Progress

---

# 📜 License

This project is developed for educational and internship purposes.