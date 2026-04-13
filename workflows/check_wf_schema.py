import sqlite3, json, uuid, os
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("PRAGMA table_info(workflow_entity)")
cols = [r[1] for r in cur.fetchall()]
print("workflow_entity columns:", cols)

db.close()
