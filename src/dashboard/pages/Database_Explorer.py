import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Database Explorer",
    layout="wide"
)

st.title("🗄️ Database Explorer")

# Connect Database
conn = sqlite3.connect("data/nifty100.db")

try:

    # Get all table names
    tables = pd.read_sql(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
        """,
        conn
    )

    st.subheader("Available Tables")

    st.dataframe(
        tables,
      use_container_width=True
    )

    table_name = st.selectbox(
        "Select Table",
        tables["name"]
    )

    # Row Count
    count_query = f"SELECT COUNT(*) as total_rows FROM {table_name}"
    count_df = pd.read_sql(count_query, conn)

    st.metric(
        "Total Rows",
        int(count_df.iloc[0]["total_rows"])
    )

    # Preview Data
    st.subheader(f"Preview: {table_name}")

    preview_df = pd.read_sql(
        f"SELECT * FROM {table_name} LIMIT 100",
        conn
    )

    st.dataframe(
        preview_df,
        use_container_width=True
    )

    # Column Information
    st.subheader("Column Information")

    columns_df = pd.read_sql(
        f"PRAGMA table_info({table_name})",
        conn
    )

    st.dataframe(
        columns_df,
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

finally:
    conn.close()