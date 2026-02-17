import sqlite3 as sq

with sq.connect("testdata.db") as conn:
    cur = conn.cursor()
    cur.execute("""
    """)