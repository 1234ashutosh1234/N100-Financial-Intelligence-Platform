import sqlite3

def test_connection():

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    assert conn is not None