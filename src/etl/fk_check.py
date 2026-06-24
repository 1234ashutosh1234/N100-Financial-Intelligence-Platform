import sqlite3

conn = sqlite3.connect("data/nifty100.db")

cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_key_check"
)

rows = cursor.fetchall()

print(rows)

if len(rows) == 0:
    print("FK CHECK PASSED")
else:
    print("FK ISSUES FOUND")

conn.close()