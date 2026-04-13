#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT * FROM activation_errors")
for r in cur.fetchall():
    print(f"  {r}")

conn.close()
