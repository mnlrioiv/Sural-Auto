import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT id, workflowId, status, finished, startedAt FROM execution_entity ORDER BY startedAt DESC LIMIT 10"
)
for r in cur.fetchall():
    print(f"exec={r[0][:8]} wf={r[1][:8]} status={r[2]} finished={r[3]} started={r[4]}")
db.close()
