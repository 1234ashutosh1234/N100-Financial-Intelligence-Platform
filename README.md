# 📈 N100 Financial Intelligence Platform

## Overview

The N100 Financial Intelligence Platform is a comprehensive financial analytics and investment intelligence system designed to analyze Nifty 100 companies using financial statements, stock price history, sector classification, and key financial ratios.

The platform integrates data engineering, analytics, visualization, and reporting capabilities into a single Streamlit-based dashboard powered by SQLite and Python.

---

## 🚀 Features

### Data Engineering & ETL

* Automated Excel data ingestion
* Data normalization and validation
* SQLite database integration
* Load audit generation
* Data quality checks

### Financial Analytics

* Profitability Analysis
* Risk Analysis
* Growth Analysis
* Valuation Analysis
* Financial Health Scoring
* Company Ranking Engine

### Investment Intelligence

* Stock Screening
* Recommendation Engine
* Peer Comparison
* Sector Ranking
* Company Scorecards

### Interactive Dashboard

* Company Analysis
* Database Explorer
* Sector Analytics
* Stock Screener
* Investment Recommendations

### Reporting

* Automated PDF Report Generation
* Validation Reports
* Load Audit Reports

---

## 🏗️ Project Architecture

```text
N100-FINANCIAL-INTELLIGENCE-PLATFORM
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── nifty100.db
│
├── db/
│   └── schema.sql
│
├── output/
│   ├── load_audit.csv
│   ├── validation_failures.csv
│   ├── company_health_scores.csv
│   └── top_recommendations.csv
│
├── reports/
│   └── company_report.pdf
│
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   ├── api/
│   └── reporting/
│
├── tests/
│   └── etl/
│
├── requirements.txt
├── README.md
└── .env
```

---

## 📊 Database Statistics

| Metric              | Value |
| ------------------- | ----- |
| Companies           | 92    |
| Financial Ratios    | 1184  |
| Stock Price Records | 5520  |
| Database Tables     | 11    |
| Validation Rules    | 16    |
| Unit Tests          | 35+   |

---

## 🛠️ Technology Stack

### Programming Language

* Python 3.x

### Database

* SQLite

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly
* Streamlit

### Reporting

* ReportLab

### Version Control

* Git
* GitHub

---

## 📂 Core Datasets

### Primary Datasets

* companies.xlsx
* profitandloss.xlsx
* balancesheet.xlsx
* cashflow.xlsx
* analysis.xlsx
* documents.xlsx
* prosandcons.xlsx

### Supplementary Datasets

* sectors.xlsx
* stock_prices.xlsx
* financial_ratios.xlsx
* market_cap.xlsx
* peer_groups.xlsx

---

## ⚙️ Installation

Clone Repository

```bash
git clone https://github.com/1234ashutosh1234/N100-Financial-Intelligence-Platform.git
```

Navigate to Project

```bash
cd N100-Financial-Intelligence-Platform
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

## 📈 Analytics Modules

### Company Analysis

Provides company-level financial performance analysis.

### Health Score Engine

Generates company health scores based on multiple financial indicators.

### Recommendation Engine

Ranks companies based on profitability and investment metrics.

### Sector Analytics

Analyzes sector-wise company distribution and performance.

### Peer Comparison

Compares companies against industry peers.

### Stock Screener

Filters investment opportunities using financial criteria.

---

## 🧪 Data Quality Framework

Implemented 16 Data Quality Rules including:

* Missing Data Detection
* Negative ROE Validation
* Duplicate Company Validation
* Missing Sector Validation
* Missing Website Validation
* Financial Ratio Validation

Outputs:

```text
output/validation_failures.csv
output/load_audit.csv
```

---

## 📑 Deliverables

* SQLite Database
* Streamlit Dashboard
* Financial Analytics Engine
* Recommendation Engine
* Sector Analytics
* PDF Reporting System
* Validation Framework
* GitHub Repository

---

## 🎯 Sprint 1 Status

### Sprint 1 – Data Foundation

✅ Database Created

✅ ETL Pipeline Completed

✅ Data Validation Framework Completed

✅ Load Audit Completed

✅ Streamlit Dashboard Completed

✅ Analytics Modules Integrated

✅ PDF Reporting Implemented

✅ GitHub Repository Published

---

## 👨‍💻 Author

**Ashutosh Raj**

B.Tech Student
Bihar Engineering University, Patna

GitHub:
https://github.com/1234ashutosh1234

LinkedIn:
https://www.linkedin.com/in/ashutosh-raj-90740731a/

---

## 📄 License

This project is developed for educational, research, and portfolio purposes.

# 
