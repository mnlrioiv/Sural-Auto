#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DELETE FROM settings WHERE key = 'userManagement.isInstanceOwnerSetUp'")
cur.execute(
    "INSERT INTO settings (key, value) VALUES ('userManagement.isInstanceOwnerSetUp', 'true')"
)

conn.commit()
print("Done")
conn.close()
