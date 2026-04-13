import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("PRAGMA table_info(workflow_dependency)")
cols = [r[1] for r in cur.fetchall()]
print("workflow_dependency cols:", cols)
db.close()
