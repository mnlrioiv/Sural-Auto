#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("UPDATE workflow_entity SET active = 1 WHERE id = 1")
conn.commit()
print("Workflow activated")
cur.execute("SELECT id, name, active FROM workflow_entity")
for row in cur.fetchall():
    print(row)
conn.close()
