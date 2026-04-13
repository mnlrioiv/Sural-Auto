#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT id, email, firstName, lastName, roleSlug, settings FROM user")
for r in cur.fetchall():
    print(f"User: {r}")

cur.execute("SELECT id, userId, label, scopes, audience FROM user_api_keys")
for r in cur.fetchall():
    print(f"API Key: {r}")

conn.close()
