import sqlite3
import pandas as pd

DB = "data/nifty100.db"


def get_connection():
    return sqlite3.connect(DB)


def query(sql):

    conn = get_connection()

    df = pd.read_sql(sql, conn)

    conn.close()

    return df