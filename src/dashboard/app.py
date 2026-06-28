
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    layout="wide"
)

# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "nifty100.db"

if not DB_PATH.exists():
    st.error(f"Database not found: {DB_PATH}")
    st.stop()

conn = sqlite3.connect(DB_PATH)
# -----------------------------------------
# HEADER
# -----------------------------------------
st.title("📈 N100 Financial Intelligence Platform")

companies = pd.read_sql(
    "SELECT COUNT(*) total FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT COUNT(*) total FROM financial_ratios",
    conn
)

prices = pd.read_sql(
    "SELECT COUNT(*) total FROM stock_prices",
    conn
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", int(companies.iloc[0, 0]))
c2.metric("Database Tables", 12)
c3.metric("Financial Ratios", int(ratios.iloc[0, 0]))
c4.metric("Stock Prices", int(prices.iloc[0, 0]))

st.success("Database Connected Successfully")

st.divider()

# -----------------------------------------
# SIDEBAR
# -----------------------------------------
st.sidebar.title("🔍 Company Search")

company_list = pd.read_sql(
    """
    SELECT DISTINCT company_id
    FROM financial_ratios
    ORDER BY company_id
    """,
    conn
)

selected_company = st.sidebar.selectbox(
    "Select Company",
    company_list["company_id"]
)

# -----------------------------------------
# COMPANY DATA
# -----------------------------------------
company_data = pd.read_sql(
    f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id='{selected_company}'
    ORDER BY year
    """,
    conn
)

st.subheader(f"📊 {selected_company} Financial Analysis")

st.dataframe(
    company_data,
    use_container_width=True
)

# -----------------------------------------
# ROE TREND
# -----------------------------------------
if "return_on_equity_pct" in company_data.columns:

    fig1 = px.line(
        company_data,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title=f"{selected_company} ROE Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------
# DEBT TO EQUITY
# -----------------------------------------
if "debt_to_equity" in company_data.columns:

    fig2 = px.bar(
        company_data,
        x="year",
        y="debt_to_equity",
        title=f"{selected_company} Debt to Equity Ratio"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------
# NET PROFIT MARGIN
# -----------------------------------------
if "net_profit_margin_pct" in company_data.columns:

    fig3 = px.line(
        company_data,
        x="year",
        y="net_profit_margin_pct",
        markers=True,
        title=f"{selected_company} Net Profit Margin"
    )

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------
# OPERATING PROFIT MARGIN
# -----------------------------------------
if "operating_profit_margin_pct" in company_data.columns:

    fig4 = px.line(
        company_data,
        x="year",
        y="operating_profit_margin_pct",
        markers=True,
        title=f"{selected_company} Operating Profit Margin"
    )

    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------
# LATEST SNAPSHOT
# -----------------------------------------
st.subheader("📌 Latest Financial Snapshot")

st.dataframe(
    company_data.tail(1),
    use_container_width=True
)

# -----------------------------------------
# TOP ROE
# -----------------------------------------
st.subheader("🏆 Top 10 ROE Companies")

top_roe = pd.read_sql(
    """
    SELECT company_id,
           year,
           return_on_equity_pct
    FROM financial_ratios
    ORDER BY return_on_equity_pct DESC
    LIMIT 10
    """,
    conn
)

st.dataframe(top_roe, use_container_width=True)

# -----------------------------------------
# HEALTH SCORE
# -----------------------------------------
st.subheader("💪 Top Health Score Companies")

try:

    health_df = pd.read_csv(
        "output/company_health_scores.csv"
    )

    st.dataframe(
        health_df.head(10),
        use_container_width=True
    )

    fig_health = px.bar(
        health_df.head(10),
        x="company_id",
        y="Health_Score",
        title="Top 10 Health Score Companies"
    )

    st.plotly_chart(
        fig_health,
        use_container_width=True
    )

except:
    st.warning("Run health_score.py first")

# -----------------------------------------
# STOCK SCREENER
# -----------------------------------------
st.subheader("🔍 Stock Screener Results")

try:

    screener_df = pd.read_csv(
        "output/stock_screener.csv"
    )

    st.dataframe(
        screener_df,
        use_container_width=True
    )

except:
    st.warning("Run screener.py first")

# -----------------------------------------
# PEER COMPARISON
# -----------------------------------------
st.subheader("🤝 Peer Comparison")

try:

    peer_df = pd.read_csv(
        "output/peer_comparison.csv"
    )

    st.dataframe(
        peer_df.head(20),
        use_container_width=True
    )

except:
    st.warning("Run peer_comparison.py first")

# -----------------------------------------
# SECTOR RANKING
# -----------------------------------------
st.subheader("🏭 Sector Ranking")

try:

    sector_df = pd.read_csv(
        "output/sector_ranking.csv"
    )

    st.dataframe(
        sector_df,
        use_container_width=True
    )

    fig_sector = px.bar(
        sector_df,
        x=sector_df.columns[0],
        y="Companies",
        title="Sector Wise Company Distribution"
    )

    st.plotly_chart(
        fig_sector,
        use_container_width=True
    )

except:
    st.warning("Run sector_ranking.py first")

# -----------------------------------------
# INVESTMENT RECOMMENDATIONS
# -----------------------------------------
st.subheader("⭐ Top Investment Recommendations")

try:

    rec_df = pd.read_csv(
        "output/top_recommendations.csv"
    )

    st.dataframe(
        rec_df,
        use_container_width=True
    )

    fig_rec = px.bar(
        rec_df.head(10),
        x="company_id",
        y="avg_roe",
        title="Top Investment Recommendations"
    )

    st.plotly_chart(
        fig_rec,
        use_container_width=True
    )

except:
    st.warning(
        "Run recommendation_engine.py first"
    )

# -----------------------------------------
# PDF DOWNLOAD
# -----------------------------------------
st.subheader("📄 Download PDF Report")

if os.path.exists(
    "reports/company_report.pdf"
):

    with open(
        "reports/company_report.pdf",
        "rb"
    ) as pdf_file:

        st.download_button(
            label="📥 Download Company Report",
            data=pdf_file,
            file_name="company_report.pdf",
            mime="application/pdf"
        )

# -----------------------------------------
# FINANCIAL RATIOS PREVIEW
# -----------------------------------------
st.subheader("📑 Financial Ratios Dataset")

ratio_preview = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    LIMIT 20
    """,
    conn
)

st.dataframe(
    ratio_preview,
    use_container_width=True
)

# -----------------------------------------
# COMPANIES PREVIEW
# -----------------------------------------
st.subheader("🏢 Companies Dataset")

company_preview = pd.read_sql(
    """
    SELECT *
    FROM companies
    LIMIT 20
    """,
    conn
)

st.dataframe(
    company_preview,
    use_container_width=True
)

# -----------------------------------------
# PROJECT SUMMARY
# -----------------------------------------
st.markdown("---")

st.subheader("📌 Project Summary")

summary_df = pd.DataFrame({
    "Metric": [
        "Companies",
        "Database Tables",
        "Financial Ratios",
        "Stock Prices"
    ],
    "Value": [
        int(companies.iloc[0, 0]),
        12,
        int(ratios.iloc[0, 0]),
        int(prices.iloc[0, 0])
    ]
})

st.dataframe(
    summary_df,
    use_container_width=True
)

st.success(
    "🚀 N100 Financial Intelligence Platform - Day 10 Portfolio Version"
)

conn.close()

