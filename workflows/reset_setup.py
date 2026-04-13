#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DELETE FROM user")
cur.execute("DELETE FROM user_api_keys")
cur.execute("DELETE FROM project_relation")
cur.execute("DELETE FROM settings WHERE key = 'userManagement.isInstanceOwnerSetUp'")
conn.commit()
print("Reset user setup. isInstanceOwnerSetUp should now be false.")
conn.close()
