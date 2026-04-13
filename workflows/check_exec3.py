import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT id, workflowId, status, finished, startedAt FROM execution_entity ORDER BY startedAt DESC LIMIT 10"
)
for r in cur.fetchall():
    exec_id = str(r[0])
    wf_id = str(r[1])
    print(
        f"exec={exec_id[:8]} wf={wf_id[:8]} status={r[2]} finished={r[3]} started={r[4]}"
    )
db.close()
