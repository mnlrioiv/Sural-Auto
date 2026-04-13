#!/usr/bin/env python3
import sqlite3
import hashlib
import secrets
import string

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT key, value FROM settings")
for r in cur.fetchall():
    print(f"Setting: {r}")

conn.close()
