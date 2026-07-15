import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.db import (
    get_peer_percentiles,
)

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

st.title("👥 Peer Comparison Dashboard")

peer = get_peer_percentiles()

# ------------------------
# Company Selection
# ------------------------

company = st.selectbox(
    "Select Company",
    sorted(peer["company_id"].unique())
)

year = st.selectbox(
    "Select Year",
    sorted(peer["year"].unique())
)

df = peer[
    (peer["company_id"] == company)
    &
    (peer["year"] == year)
]

st.divider()

if len(df) == 0:

    st.warning("No Data Found")

else:

    row = df.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ROE Percentile",
        f'{row["return_on_equity_pct_rank"]:.2f}'
    )

    c2.metric(
        "ROCE Percentile",
        f'{row["roce_pct_rank"]:.2f}'
    )

    c3.metric(
        "Debt/Equity Percentile",
        f'{row["debt_to_equity_rank"]:.2f}'
    )

    st.divider()

    st.subheader("Complete Peer Percentiles")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

st.subheader("📊 Peer Performance Radar Chart")

metrics = [
    "return_on_equity_pct_rank",
    "roce_pct_rank",
    "net_profit_margin_pct_rank",
    "debt_to_equity_rank",
    "free_cash_flow_cr_rank",
    "sales_cagr_pct_rank",
    "profit_cagr_pct_rank",
    "eps_cagr_pct_rank",
]

labels = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "Sales CAGR",
    "Profit CAGR",
    "EPS CAGR",
]

values = [
    row[m] for m in metrics
]

# Close the radar chart
values.append(values[0])
labels.append(labels[0])

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        name=company,
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
        )
    ),
    showlegend=False,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)