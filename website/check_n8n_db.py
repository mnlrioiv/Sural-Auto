#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables:", [t[0] for t in tables])

for t in tables:
    name = t[0]
    try:
        cur.execute(f"PRAGMA table_info({name})")
        cols = cur.fetchall()
        print(f"\n{name}: {[c[1] for c in cols]}")
    except:
        pass

conn.close()
