import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT * FROM shared_workflow")
for r in cur.fetchall():
    print(r)

cur.execute("SELECT id, name FROM workflow_entity")
for r in cur.fetchall():
    print(f"wf: {r[0][:8]} | {r[1]}")
db.close()
